from django.contrib import admin
from .models import ImageLink, Contact


@admin.register(ImageLink)
class ImageLinkAdmin(admin.ModelAdmin):
    """Admin interface for Image Links"""
    
    list_display = ['original_filename', 'expiry_duration', 'view_count', 'created_at', 'expires_at', 'is_expired']
    list_filter = ['expiry_duration', 'created_at']
    search_fields = ['original_filename', 'link_id']
    readonly_fields = ['link_id', 'created_at', 'view_count']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('image', 'original_filename', 'link_id')
        }),
        ('Expiration Settings', {
            'fields': ('expiry_duration', 'expires_at', 'created_at')
        }),
        ('Statistics', {
            'fields': ('view_count',)
        }),
    )
    
    def is_expired(self, obj):
        """Show if link is expired"""
        if obj.is_expired():
            return '❌ Expired'
        return '✅ Active'
    is_expired.short_description = 'Status'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact Messages"""
    
    list_display = ['name', 'email', 'message_type', 'subject', 'status', 'created_at', 'is_new']
    list_filter = ['message_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('message_type', 'subject', 'message', 'attachment')
        }),
        ('Status & Management', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_in_progress', 'mark_as_resolved', 'mark_as_closed']
    
    def mark_as_in_progress(self, request, queryset):
        """Mark selected messages as in progress"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} message(s) marked as in progress.')
    mark_as_in_progress.short_description = 'Mark as In Progress'
    
    def mark_as_resolved(self, request, queryset):
        """Mark selected messages as resolved"""
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} message(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark as Resolved'
    
    def mark_as_closed(self, request, queryset):
        """Mark selected messages as closed"""
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} message(s) marked as closed.')
    mark_as_closed.short_description = 'Mark as Closed'
    
    def is_new(self, obj):
        """Highlight new messages"""
        if obj.is_new():
            return '🔴 NEW'
        return '✅ Read'
    is_new.short_description = 'New?'