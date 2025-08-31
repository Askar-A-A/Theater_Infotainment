"""
Custom Admin Widgets

This module contains custom form widgets for the Theater CMS admin interface.
"""

from django import forms
from django.utils.safestring import mark_safe


class CustomFileInput(forms.FileInput):
    """
    Custom file input widget that shows current file and new file selection
    without the clear checkbox functionality.
    """
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        
    def render(self, name, value, attrs=None, renderer=None):
        # Get the basic file input
        html = super().render(name, value, attrs, renderer)
        
        # Generate unique timestamp for this widget instance
        import time
        timestamp = str(int(time.time() * 1000))
        
        # Add current file display if file exists
        current_file_html = ""
        if value and hasattr(value, 'url'):
            current_file_html = f"""
            <div style="margin-top: 5px;">
                <div style="display: inline-block; background: #e3f2fd; padding: 5px 10px; border-radius: 4px; border: 1px solid #2196f3;">
                    <strong>Current:</strong> <a href="{value.url}" target="_blank" style="color: #1976d2; text-decoration: none;">{value.name.split('/')[-1]}</a>
                </div>
            </div>
            """
        
        # Add container for selected file display
        selected_file_html = f"""
        <div id="selected-file-{timestamp}" style="margin-top: 5px; display: none;">
            <div style="display: inline-block; background: #e8f5e8; padding: 5px 10px; border-radius: 4px; border: 1px solid #4caf50;">
                <strong>Selected:</strong> <span id="filename-{timestamp}" style="color: #2e7d32;"></span>
            </div>
        </div>
        """
        
        # JavaScript to handle file selection display
        javascript = f"""
        <script>
        (function() {{
            var timestamp = '{timestamp}';
            
            function initFileDisplay() {{
                // Find the file input - it might be in a regular form or inline form
                var fileInput = document.querySelector('input[name="{name}"]');
                if (!fileInput) return;
                
                // Avoid double initialization
                if (fileInput.hasAttribute('data-custom-initialized-' + timestamp)) return;
                fileInput.setAttribute('data-custom-initialized-' + timestamp, 'true');
                
                var selectedDiv = document.getElementById('selected-file-' + timestamp);
                var filenameSpan = document.getElementById('filename-' + timestamp);
                
                if (!selectedDiv || !filenameSpan) return;
                
                fileInput.addEventListener('change', function() {{
                    if (this.files && this.files[0]) {{
                        filenameSpan.textContent = this.files[0].name;
                        selectedDiv.style.display = 'block';
                    }} else {{
                        selectedDiv.style.display = 'none';
                    }}
                }});
            }}
            
            // Initialize immediately if DOM is ready
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', initFileDisplay);
            }} else {{
                initFileDisplay();
            }}
            
            // Also initialize after a short delay for dynamic content
            setTimeout(initFileDisplay, 100);
            setTimeout(initFileDisplay, 500);
            setTimeout(initFileDisplay, 1000);
            
            // Watch for dynamically added forms (like inline forms)
            if (typeof MutationObserver !== 'undefined') {{
                var observer = new MutationObserver(function(mutations) {{
                    mutations.forEach(function(mutation) {{
                        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {{
                            setTimeout(initFileDisplay, 50);
                        }}
                    }});
                }});
                
                observer.observe(document.body, {{
                    childList: true,
                    subtree: true
                }});
            }}
        }})();
        </script>
        """
        
        return mark_safe(html + current_file_html + selected_file_html + javascript)
