"""
CMS Backup Service

This module handles all backup and restore operations for the Theater CMS.
Provides functions for creating, restoring, listing, and deleting CMS backups.
"""

import os
import datetime
import tempfile
import json
import shutil
from django.conf import settings
from django.core import serializers
from django.apps import apps
from django.db import transaction


def backup_cms_data(notes=""):
    """Create a backup of all CMS data with optimized memory usage"""
    
    try:
        # Create backups directory if it doesn't exist
        backup_dir = os.path.join(settings.BASE_DIR, 'cms_backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'cms_backup_{timestamp}.json')
        
        # Get all models from the apps we want to backup
        models_to_backup = []
        app_labels = ['cms', 'djangocms_text_ckeditor', 'djangocms_picture', 'filer', 'theater_cms']
        
        for app_label in app_labels:
            try:
                app_config = apps.get_app_config(app_label)
                app_models = list(app_config.get_models())  # Convert generator to list
                models_to_backup.extend(app_models)
                print(f"Backup: Including {len(app_models)} models from {app_label}")
                
                # Log specific models that might contain Q&A content
                for model in app_models:
                    if 'placeholder' in model.__name__.lower() or 'plugin' in model.__name__.lower():
                        print(f"  - {model.__name__} (potential Q&A container)")
                        
            except LookupError:
                # App not installed, skip it
                print(f"Backup: App {app_label} not found, skipping")
                continue
        
        # Use temporary file first, then move to final location for atomic operation
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name
            
            # Stream objects directly to file to avoid memory issues with large datasets
            temp_file.write('[\n')
            first_object = True
            object_count = 0
            
            for model in models_to_backup:
                try:
                    # Process in chunks to avoid memory issues
                    queryset = model.objects.all()
                    
                    for obj in queryset.iterator(chunk_size=100):  # Process in batches
                        try:
                            # Serialize individual object
                            serialized = serializers.serialize('json', [obj], ensure_ascii=False)
                            # Remove the array brackets and add to our stream
                            obj_data = json.loads(serialized)[0]
                            
                            if not first_object:
                                temp_file.write(',\n')
                            
                            json.dump(obj_data, temp_file, ensure_ascii=False, indent=2)
                            first_object = False
                            object_count += 1
                            
                        except Exception as e:
                            # Skip problematic objects
                            print(f"Skipping object {obj}: {e}")
                            continue
                            
                except Exception as e:
                    # Skip problematic models
                    print(f"Skipping model {model}: {e}")
                    continue
            
            temp_file.write('\n]')
        
        # Validate the temporary file
        try:
            with open(temp_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            # Remove corrupted file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return None, f"Created backup file is corrupted: {str(e)}"
        
        # Check if we actually backed up some data
        if object_count == 0:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return None, "No data found to backup"
        
        # Check file size
        file_size = os.path.getsize(temp_path)
        if file_size < 50:  # Very small file likely means error
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return None, f"Backup file too small, likely an error: {content[:200]}"
        
        # Atomic move to final location
        shutil.move(temp_path, backup_file)
        
        # Create metadata file with notes and backup info
        metadata_file = backup_file.replace('.json', '_metadata.json')
        backup_metadata = {
            'backup_file': os.path.basename(backup_file),
            'created_at': datetime.datetime.now().isoformat(),
            'notes': notes.strip() if notes else "",
            'object_count': object_count,
            'file_size': os.path.getsize(backup_file),
            'apps_included': ['cms', 'djangocms_text_ckeditor', 'djangocms_picture', 'filer', 'theater_cms']
        }
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as meta_f:
                json.dump(backup_metadata, meta_f, ensure_ascii=False, indent=2)
        except Exception as meta_error:
            # Don't fail the backup if metadata creation fails
            print(f"Warning: Could not create metadata file: {meta_error}")
        
        return backup_file, f"Successfully backed up {object_count} objects"
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return None, f"Backup creation error: {str(e)}"


def restore_cms_data(backup_file):
    """Restore CMS data from backup file with optimized transaction handling"""
    
    try:
        if not os.path.exists(backup_file):
            return False, "Backup file not found"
        
        # Check file size first
        file_size = os.path.getsize(backup_file)
        if file_size < 50:
            return False, f"Backup file is too small ({file_size} bytes) - likely corrupted"
        
        # Validate JSON format first with detailed error info
        backup_data = None
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    return False, "Backup file is empty"
                
                # Try to parse JSON and store it
                backup_data = json.loads(content)
                if not isinstance(backup_data, list):
                    return False, "Invalid backup format - expected list of objects"
                
        except json.JSONDecodeError as e:
            # Provide more detailed error information
            line_num = getattr(e, 'lineno', 'unknown')
            col_num = getattr(e, 'colno', 'unknown')
            char_pos = getattr(e, 'pos', 'unknown')
            
            # Show some context around the error
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    start_pos = max(0, e.pos - 50) if hasattr(e, 'pos') else 0
                    end_pos = min(len(content), e.pos + 50) if hasattr(e, 'pos') else 100
                    context = content[start_pos:end_pos]
                    
                return False, f"Backup file is corrupted at line {line_num}, column {col_num} (char {char_pos}). Context: ...{context}..."
            except:
                return False, f"Backup file is corrupted: {str(e)}"
        
        except UnicodeDecodeError as e:
            return False, f"Backup file encoding error: {str(e)}"
        
        # Restore with transaction for atomicity
        try:
            with transaction.atomic():
                # Convert back to JSON string for serializer
                json_data = json.dumps(backup_data, ensure_ascii=False)
                
                # Deserialize all objects
                objects = list(serializers.deserialize('json', json_data))
                
                if not objects:
                    return False, "No valid objects found in backup file"
                
                # Sort objects by dependency order (models that don't depend on others first)
                # This helps avoid foreign key constraint errors
                dependency_order = [
                    'auth.user', 'auth.group', 'auth.permission',
                    'sites.site',
                    'filer.folder', 'filer.file', 'filer.image',
                    'cms.page', 'cms.placeholder', 'cms.cmsplugin',
                    'djangocms_text_ckeditor.text',
                    'djangocms_picture.picture',
                    'theater_cms.'  # All theater_cms models
                ]
                
                def get_sort_key(obj):
                    model_name = f"{obj.object._meta.app_label}.{obj.object._meta.model_name}"
                    for i, pattern in enumerate(dependency_order):
                        if model_name.startswith(pattern):
                            return i
                    return len(dependency_order)  # Unknown models last
                
                objects.sort(key=get_sort_key)
                
                # Save objects in order
                saved_count = 0
                skipped_count = 0
                
                for obj in objects:
                    try:
                        obj.save()
                        saved_count += 1
                    except Exception as e:
                        # Log but continue with other objects
                        skipped_count += 1
                        print(f"Skipping object {obj.object._meta.model_name} (ID: {obj.object.pk}): {e}")
                        continue
            
            return True, f"CMS data restored successfully. Saved: {saved_count}, Skipped: {skipped_count} objects"
            
        except Exception as e:
            # More specific error handling
            error_msg = str(e)
            if "DoesNotExist" in error_msg:
                return False, "Backup contains references to missing data. Try creating a fresh backup."
            elif "IntegrityError" in error_msg:
                return False, "Database integrity error. The backup may be incompatible with current database structure."
            elif "ValidationError" in error_msg:
                return False, "Data validation error. The backup data may be corrupted."
            else:
                return False, f"Restore failed: {error_msg[:300]}..."
                
    except Exception as e:
        return False, f"Unexpected error: {str(e)[:300]}..."


def get_backup_files():
    """Get list of available backup files with metadata"""
    backup_dir = os.path.join(settings.BASE_DIR, 'cms_backups')
    if not os.path.exists(backup_dir):
        return []
    
    files = []
    for filename in os.listdir(backup_dir):
        if filename.startswith('cms_backup_') and filename.endswith('.json') and not filename.endswith('_metadata.json'):
            filepath = os.path.join(backup_dir, filename)
            metadata_path = filepath.replace('.json', '_metadata.json')
            file_stat = os.stat(filepath)
            
            # Try to read metadata
            metadata = {}
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as meta_f:
                        metadata = json.load(meta_f)
                except Exception:
                    # If metadata is corrupted, continue with basic info
                    pass
            
            file_info = {
                'name': filename,
                'path': filepath,
                'size': file_stat.st_size,
                'date': datetime.datetime.fromtimestamp(file_stat.st_mtime),
                'notes': metadata.get('notes', ''),
                'object_count': metadata.get('object_count', 0),
                'metadata_exists': os.path.exists(metadata_path)
            }
            
            files.append(file_info)
    
    # Sort by date, newest first
    files.sort(key=lambda x: x['date'], reverse=True)
    return files


def delete_backup_file(backup_filename):
    """Delete a backup file and its metadata"""
    try:
        print(f"DELETE_BACKUP: Starting deletion of {backup_filename}")
        
        backup_dir = os.path.join(settings.BASE_DIR, 'cms_backups')
        backup_path = os.path.join(backup_dir, backup_filename)
        metadata_path = backup_path.replace('.json', '_metadata.json')
        
        print(f"DELETE_BACKUP: Backup path: {backup_path}")
        print(f"DELETE_BACKUP: Metadata path: {metadata_path}")
        
        # Check if backup file exists
        if not os.path.exists(backup_path):
            print(f"DELETE_BACKUP: ERROR - Backup file not found: {backup_path}")
            return False, f"Backup file not found: {backup_filename}"
        
        # Validate filename for security
        if not backup_filename.startswith('cms_backup_') or not backup_filename.endswith('.json'):
            print(f"DELETE_BACKUP: ERROR - Invalid filename format: {backup_filename}")
            return False, f"Invalid backup filename format: {backup_filename}"
        
        # Delete backup file
        print(f"DELETE_BACKUP: Deleting backup file...")
        os.remove(backup_path)
        print(f"DELETE_BACKUP: ✅ Backup file deleted successfully")
        
        # Delete metadata file if it exists
        if os.path.exists(metadata_path):
            print(f"DELETE_BACKUP: Deleting metadata file...")
            os.remove(metadata_path)
            print(f"DELETE_BACKUP: ✅ Metadata file deleted successfully")
        else:
            print(f"DELETE_BACKUP: No metadata file to delete")
        
        # Verify deletion
        if os.path.exists(backup_path):
            print(f"DELETE_BACKUP: ERROR - Backup file still exists after deletion!")
            return False, "Failed to delete backup file - file still exists"
        
        print(f"DELETE_BACKUP: ✅ Deletion completed successfully")
        return True, f"Backup '{backup_filename}' deleted successfully"
        
    except PermissionError as e:
        error_msg = f"Permission denied deleting backup: {str(e)}"
        print(f"DELETE_BACKUP: ERROR - {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Error deleting backup: {str(e)}"
        print(f"DELETE_BACKUP: ERROR - {error_msg}")
        return False, error_msg
