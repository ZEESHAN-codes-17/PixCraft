from django.db import models
from django.utils import timezone
import uuid
import os
import hashlib
from datetime import datetime


def encrypted_upload_path(instance, filename):
    """
    Generate encrypted filename for uploaded images
    This prevents identifying user images by filename
    """
    # Get file extension
    ext = os.path.splitext(filename)[1].lower()
    
    # Create unique encrypted filename using UUID + timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    unique_string = f"{uuid.uuid4()}{timestamp}"
    encrypted_name = hashlib.sha256(unique_string.encode()).hexdigest()
    
    # Return path with encrypted filename
    return f'temp_images/{encrypted_name}{ext}'


class ImageLink(models.Model):
    """Model for temporary shareable image links"""
    
    # Unique ID for the link
    link_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    
    # Image file (with encrypted filename)
    image = models.ImageField(upload_to=encrypted_upload_path)
    
    # Original filename (stored separately, not used in filesystem)
    original_filename = models.CharField(max_length=255)
    
    # Expiration options
    EXPIRY_CHOICES = [
        ('1h', '1 Hour'),
        ('1d', '1 Day'),
        ('7d', '7 Days'),
        ('1m', '1 Month'),
    ]
    expiry_duration = models.CharField(max_length=2, choices=EXPIRY_CHOICES, default='1d')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    # View count (optional - track how many times link was accessed)
    view_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.original_filename} - Expires: {self.expires_at}"
    
    def is_expired(self):
        """Check if the link has expired"""
        return timezone.now() > self.expires_at
    
    def get_share_url(self):
        """Get the shareable URL"""
        return f"/view-image/{self.link_id}/"
    
    def delete_image_file(self):
        """Delete the actual image file from storage"""
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)


# ============================================
# CONTACT / COMPLAINT MODEL
# ============================================
class Contact(models.Model):
    """Model for contact form submissions and complaints"""
    
    MESSAGE_TYPE_CHOICES = [
        ('contact', 'General Contact'),
        ('complaint', 'Complaint'),
        ('feedback', 'Feedback'),
        ('bug', 'Bug Report'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    # User Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    # Message Details
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='contact')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Optional Screenshot/Attachment (NOT encrypted - you need to see bug reports)
    attachment = models.ImageField(upload_to='contact_attachments/', blank=True, null=True)
    
    # Status Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin Notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes (not visible to user)")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def is_new(self):
        """Check if message is new"""
        return self.status == 'new'