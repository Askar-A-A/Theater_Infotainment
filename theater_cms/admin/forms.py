"""
Custom Admin Forms

This module contains custom form classes and validation logic for the Theater CMS admin interface.
"""

from django import forms
from theater_cms.models import Event, SeasonalSponsor, EventSponsorImage
from .widgets import CustomFileInput


class EventForm(forms.ModelForm):
    """Custom form for Event model with image upload functionality"""
    
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'image': CustomFileInput(),
        }
    
    def clean_image(self):
        """Preserve existing image if no new image is uploaded during validation errors"""
        image = self.cleaned_data.get('image')
        
        # If no new image was uploaded but instance exists and has an image, keep the existing one
        if not image and self.instance and self.instance.pk and self.instance.image:
            return self.instance.image
        
        return image


class SeasonalSponsorForm(forms.ModelForm):
    """Custom form for SeasonalSponsor model with mandatory image validation"""
    
    class Meta:
        model = SeasonalSponsor
        fields = '__all__'
        widgets = {
            'image': CustomFileInput(),
        }
    
    def clean_image(self):
        """Validate that an image is provided and preserve existing image during validation errors"""
        image = self.cleaned_data.get('image')
        
        # If no new image was uploaded but instance exists and has an image, keep the existing one
        if not image and self.instance and self.instance.pk and self.instance.image:
            return self.instance.image
        
        # For new instances or when explicitly removing an image, require an image
        if not image:
            raise forms.ValidationError("An image is required for sponsors.")
        
        return image
    
    def clean(self):
        """Preserve uploaded image during other validation errors"""
        cleaned_data = super().clean()
        
        # If there are any validation errors and an image was uploaded,
        # make sure to preserve it in the form
        if self.errors and 'image' in self.files:
            # Store the uploaded file in cleaned_data so it's not lost
            cleaned_data['image'] = self.files['image']
        
        return cleaned_data


class EventSponsorImageForm(forms.ModelForm):
    """Custom form for EventSponsorImage model with mandatory image validation"""
    
    class Meta:
        model = EventSponsorImage
        fields = '__all__'
        widgets = {
            'image': CustomFileInput(),
        }
    
    def clean_image(self):
        """Validate that an image is provided and preserve existing image during validation errors"""
        image = self.cleaned_data.get('image')
        
        # If no new image was uploaded but instance exists and has an image, keep the existing one
        if not image and self.instance and self.instance.pk and self.instance.image:
            return self.instance.image
        
        # For new instances or when explicitly removing an image, require an image
        if not image:
            raise forms.ValidationError("An image is required for sponsor logos.")
        
        return image
    
    def clean(self):
        """Preserve uploaded image during other validation errors"""
        cleaned_data = super().clean()
        
        # If there are any validation errors and an image was uploaded,
        # make sure to preserve it in the form
        if self.errors and 'image' in self.files:
            # Store the uploaded file in cleaned_data so it's not lost
            cleaned_data['image'] = self.files['image']
        
        return cleaned_data
