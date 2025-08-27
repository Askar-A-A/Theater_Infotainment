// Sponsor Delete Functionality with Confirmation
(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Handle delete button clicks
        $(document).on('click', '.delete-sponsor-btn', function(e) {
            e.preventDefault();
            
            const sponsorId = $(this).data('sponsor-id');
            const sponsorName = $(this).data('sponsor-name');
            const modelType = $(this).data('model') || 'event'; // 'seasonal' or 'event'
            const button = $(this);
            
            // Show confirmation dialog
            const confirmMessage = `Are you sure you want to delete the sponsor "${sponsorName}"?\n\nThis action cannot be undone.`;
            
            if (confirm(confirmMessage)) {
                // Disable button during request
                button.prop('disabled', true);
                button.css('opacity', '0.5');
                
                // Determine the correct URL based on model type
                let deleteUrl;
                if (modelType === 'seasonal') {
                    deleteUrl = `/admin/theater_cms/seasonalsponsor/delete-sponsor/${sponsorId}/`;
                } else {
                    deleteUrl = `/admin/theater_cms/event/delete-event-sponsor/${sponsorId}/`;
                }
                
                // Make AJAX request
                $.ajax({
                    url: deleteUrl,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                    },
                    success: function(response) {
                        if (response.success) {
                            // Show success message
                            showMessage(response.message, 'success');
                            
                            // Remove the row from the table
                            if (modelType === 'seasonal') {
                                // For seasonal sponsors, remove the entire table row
                                button.closest('tr').fadeOut(300, function() {
                                    $(this).remove();
                                });
                            } else {
                                // For event sponsors (inline), remove the inline row
                                const inlineRow = button.closest('.dynamic-eventsponsorimage_set, .form-row');
                                inlineRow.fadeOut(300, function() {
                                    $(this).remove();
                                    // Update the total forms count
                                    updateInlineFormCount();
                                });
                            }
                        } else {
                            showMessage(response.message, 'error');
                            // Re-enable button on error
                            button.prop('disabled', false);
                            button.css('opacity', '1');
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Delete request failed:', error);
                        showMessage('Failed to delete sponsor. Please try again.', 'error');
                        // Re-enable button on error
                        button.prop('disabled', false);
                        button.css('opacity', '1');
                    }
                });
            }
        });
        
        // Hide the default Django delete checkboxes
        $('.field-DELETE').hide();
        
        // Add some styling to make trash icons more visible
        $('.delete-sponsor-btn').hover(
            function() {
                $(this).css('background-color', '#f8d7da');
                $(this).css('border-radius', '3px');
            },
            function() {
                $(this).css('background-color', 'transparent');
            }
        );
    });
    
    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Function to show messages to the user
    function showMessage(message, type) {
        // Remove existing messages
        $('.sponsor-delete-message').remove();
        
        // Create message element
        const messageClass = type === 'success' ? 'success' : 'error';
        const iconClass = type === 'success' ? '✓' : '✗';
        
        const messageHtml = `
            <div class="sponsor-delete-message ${messageClass}" style="
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                z-index: 9999;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                max-width: 400px;
                ${type === 'success' ? 'background-color: #28a745;' : 'background-color: #dc3545;'}
            ">
                <span style="margin-right: 8px;">${iconClass}</span>
                ${message}
            </div>
        `;
        
        // Add message to page
        $('body').append(messageHtml);
        
        // Auto-remove after 4 seconds
        setTimeout(function() {
            $('.sponsor-delete-message').fadeOut(300, function() {
                $(this).remove();
            });
        }, 4000);
    }
    
    // Function to update inline form count after deletion
    function updateInlineFormCount() {
        const prefix = 'sponsor_images';
        const totalFormsInput = $(`#id_${prefix}-TOTAL_FORMS`);
        if (totalFormsInput.length) {
            const currentCount = parseInt(totalFormsInput.val()) || 0;
            if (currentCount > 0) {
                totalFormsInput.val(currentCount - 1);
            }
        }
    }
    
})(django.jQuery); 