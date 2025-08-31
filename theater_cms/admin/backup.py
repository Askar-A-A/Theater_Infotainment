"""
CMS Backup Admin Interface

This module contains the backup and restore admin interface for the Theater CMS.
Provides a custom admin view for creating, downloading, restoring, and deleting CMS backups.
"""

import os
import json
from django.contrib import admin
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.urls import path
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from theater_cms.services import backup_cms_data, restore_cms_data, get_backup_files, delete_backup_file


class CMSBackupAdmin:
    """Custom admin interface for CMS backup and restore operations"""
    
    def get_urls(self):
        """Define custom URLs for backup operations"""
        urls = [
            path('cms-backup/', self.backup_view, name='cms_backup'),
            path('cms-backup/create/', self.create_backup, name='cms_backup_create'),
            path('cms-backup/restore/', self.restore_backup, name='cms_backup_restore'),
            path('cms-backup/download/<str:filename>/', self.download_backup, name='cms_backup_download'),
            path('cms-backup/delete/', self.delete_backup, name='cms_backup_delete'),
        ]
        return urls
    
    def backup_view(self, request):
        """Main backup interface view"""
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'create_backup':
                # Get backup notes from the form
                notes = request.POST.get('backup_notes', '').strip()
                
                try:
                    backup_file, message = backup_cms_data(notes)
                    if backup_file:
                        messages.success(request, f'Backup created successfully: {message}')
                    else:
                        messages.error(request, f'Backup failed: {message}')
                except Exception as e:
                    messages.error(request, f'Backup failed: {str(e)}')
            
            elif action == 'restore_backup':
                backup_filename = request.POST.get('backup_file')
                if backup_filename:
                    backup_path = os.path.join(settings.BASE_DIR, 'cms_backups', backup_filename)
                    try:
                        success, message = restore_cms_data(backup_path)
                        if success:
                            messages.success(request, f'Restore completed: {message}')
                        else:
                            messages.error(request, f'Restore failed: {message}')
                    except Exception as e:
                        messages.error(request, f'Restore failed: {str(e)}')
                else:
                    messages.error(request, 'No backup file selected for restore')
            
            elif action == 'delete_backup':
                backup_filename = request.POST.get('backup_file')
                if backup_filename:
                    try:
                        success, message = delete_backup_file(backup_filename)
                        if success:
                            messages.success(request, message)
                        else:
                            messages.error(request, message)
                    except Exception as e:
                        messages.error(request, f'Delete failed: {str(e)}')
                else:
                    messages.error(request, 'No backup file selected for deletion')
        
        # Get list of backup files
        backup_files = get_backup_files()
        
        context = {
            'title': 'CMS Backup & Restore',
            'backup_files': backup_files,
            'has_permission': True,
            'site_header': admin.site.site_header,
            'site_title': admin.site.site_title,
        }
        
        return render(request, 'admin/cms_backup.html', context)
    
    @method_decorator(csrf_exempt)
    def create_backup(self, request):
        """AJAX endpoint for creating backups"""
        if request.method == 'POST':
            try:
                # Parse JSON data
                data = json.loads(request.body)
                notes = data.get('backup_notes', '').strip()
                
                backup_file, message = backup_cms_data(notes)
                
                if backup_file:
                    return JsonResponse({
                        'success': True, 
                        'message': message,
                        'filename': os.path.basename(backup_file)
                    })
                else:
                    return JsonResponse({
                        'success': False, 
                        'message': message
                    })
                    
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid JSON data'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'message': f'Backup creation error: {str(e)}'
                })
        
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    @method_decorator(csrf_exempt)
    def restore_backup(self, request):
        """AJAX endpoint for restoring backups"""
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                backup_filename = data.get('backup_file')
                
                if not backup_filename:
                    return JsonResponse({
                        'success': False, 
                        'message': 'No backup file specified'
                    })
                
                backup_path = os.path.join(settings.BASE_DIR, 'cms_backups', backup_filename)
                success, message = restore_cms_data(backup_path)
                
                return JsonResponse({
                    'success': success, 
                    'message': message
                })
                
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid JSON data'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'message': f'Restore error: {str(e)}'
                })
        
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    def download_backup(self, request, filename):
        """Download backup file"""
        backup_dir = os.path.join(settings.BASE_DIR, 'cms_backups')
        file_path = os.path.join(backup_dir, filename)
        
        # Security check - ensure filename is safe
        if not filename.startswith('cms_backup_') or not filename.endswith('.json'):
            raise Http404("File not found")
        
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        try:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        except Exception as e:
            raise Http404(f"Error reading file: {str(e)}")
    
    @method_decorator(csrf_exempt)
    def delete_backup(self, request):
        """AJAX endpoint for deleting backups"""
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                backup_filename = data.get('backup_file')
                
                if not backup_filename:
                    return JsonResponse({
                        'success': False, 
                        'message': 'No backup file specified'
                    })
                
                success, message = delete_backup_file(backup_filename)
                
                return JsonResponse({
                    'success': success, 
                    'message': message
                })
                
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid JSON data'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'message': f'Delete error: {str(e)}'
                })
        
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


# Create instance and register with admin
cms_backup_admin = CMSBackupAdmin()

# Override admin site URLs to include our custom backup URLs
original_get_urls = admin.site.get_urls

def get_urls():
    """Override admin URLs to include backup functionality"""
    urls = original_get_urls()
    custom_urls = [
        path('cms-backup/', cms_backup_admin.backup_view, name='cms_backup'),
        path('cms-backup/create/', cms_backup_admin.create_backup, name='cms_backup_create'),
        path('cms-backup/restore/', cms_backup_admin.restore_backup, name='cms_backup_restore'),
        path('cms-backup/download/<str:filename>/', cms_backup_admin.download_backup, name='cms_backup_download'),
        path('cms-backup/delete/', cms_backup_admin.delete_backup, name='cms_backup_delete'),
    ]
    return custom_urls + urls

admin.site.get_urls = get_urls

# Override admin index to add backup link
original_index = admin.site.index

def index(request, extra_context=None):
    """Override admin index to add backup functionality link"""
    extra_context = extra_context or {}
    extra_context['show_backup_link'] = True
    extra_context['cms_backup_url'] = '/admin/cms-backup/'
    return original_index(request, extra_context)

admin.site.index = index
