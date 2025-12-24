"""Forms for image processing operations."""

from django import forms
from django.core.validators import FileExtensionValidator


class ImageUploadForm(forms.Form):
    """Generic form for uploading images."""
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        help_text='Supported formats: JPG, PNG, GIF, WEBP, BMP, TIFF'
    )


class MultiImageUploadForm(forms.Form):
    """Form for uploading multiple images."""
    
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        help_text='Select one or more images'
    )


class ImageResizeForm(forms.Form):
    """Form for image resizing operations."""
    
    image = forms.ImageField()
    width = forms.IntegerField(min_value=1, initial=800)
    height = forms.IntegerField(min_value=1, initial=600)
    maintain_aspect = forms.BooleanField(required=False, initial=True)


class ImageCompressionForm(forms.Form):
    """Form for image compression."""
    
    image = forms.ImageField()
    quality = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=85,
        help_text='Lower values = smaller file size'
    )


class ImageFormatConversionForm(forms.Form):
    """Form for image format conversion."""
    
    FORMAT_CHOICES = [
        ('PNG', 'PNG'),
        ('JPG', 'JPG'),
        ('WEBP', 'WEBP'),
        ('BMP', 'BMP'),
        ('TIFF', 'TIFF'),
        ('GIF', 'GIF'),
    ]
    
    image = forms.ImageField()
    output_format = forms.ChoiceField(choices=FORMAT_CHOICES, initial='PNG')


class ContactForm(forms.Form):
    """Form for contact/complaint submission."""
    
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    attachment = forms.FileField(required=False)
