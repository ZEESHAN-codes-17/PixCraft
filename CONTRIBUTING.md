"""
CONTRIBUTING AND DEVELOPMENT GUIDE

This guide explains how to work with the organized project structure.

UNDERSTANDING THE LAYERS:
=========================

When adding a new feature, follow this pattern:

1. Create the Model (tools/models.py)
   class MyFeature(models.Model):
       title = models.CharField(max_length=200)

2. Create the Form (tools/forms/image_forms.py)
   class MyFeatureForm(forms.Form):
       title = forms.CharField(max_length=200)

3. Create the Service (tools/services/)
   class MyFeatureService:
       @staticmethod
       def process_data(data):
           return result

4. Create Utilities if needed (tools/utils/)
   def validate_data(data):
       return is_valid

5. Create the View (tools/views.py or views_modules/)
   def my_feature_view(request):
       # Use service
       result = MyFeatureService.process_data(data)

6. Create Tests (tools/tests/)
   class MyFeatureTestCase(TestCase):
       def test_processing(self):
           pass

EXAMPLE: Adding Image Rotation Feature
======================================

1. Service (tools/services/image_processor.py - DONE)
   Already has: rotate_image() method

2. Form (tools/forms/image_forms.py - ADD)
   class ImageRotationForm(forms.Form):
       image = forms.ImageField()
       angle = forms.IntegerField(min_value=-360, max_value=360)

3. View (tools/views.py - ADD)
   @ratelimit(key='ip', rate='30/h', method='POST')
   def image_rotator(request):
       if request.method == 'POST':
           form = ImageRotationForm(request.POST, request.FILES)
           if form.is_valid():
               img = ImageProcessor.open_image(form.cleaned_data['image'])
               img = ImageProcessor.rotate_image(img, form.cleaned_data['angle'])
               # Return response

4. URL (tools/urls.py - ADD)
   path('image-rotator/', views.image_rotator, name='image_rotator'),

5. Tests (tools/tests/test_image_processor.py)
   def test_rotate_image(self):
       pass

USING THE SERVICES:
===================

From views.py:
    from tools.services import ImageProcessor
    
    image = ImageProcessor.open_image(file)
    image = ImageProcessor.rotate_image(image, 45)
    compressed = ImageProcessor.compress_image(image, quality=85)

USING UTILITIES:
================

From views.py:
    from tools.utils.validators import validate_upload
    from tools.utils.file_handlers import sanitize_filename
    
    validate_upload(file, max_size_mb=10)
    safe_name = sanitize_filename(filename)

USING CONFIGURATION:
====================

From anywhere:
    from config.settings import IMAGE_PROCESSING, RATE_LIMIT_SETTINGS
    from core.constants import MAX_IMAGE_SIZE, SUPPORTED_IMAGE_FORMATS
    
    max_quality = IMAGE_PROCESSING['default_compression_quality']

TESTING:
========

Run all tests:
    python manage.py test tools.tests

Run specific test:
    python manage.py test tools.tests.test_image_processor

Run with verbose output:
    python manage.py test tools.tests -v 2

COMMON TASKS:
=============

Add a new API endpoint:
    1. Create view in views.py or views_modules/
    2. Add URL pattern to urls.py
    3. Add form if needed in forms/
    4. Create test in tests/

Update settings:
    - App-specific: config/settings.py
    - Constants: core/constants.py
    - Exceptions: core/exceptions.py

Add new utility:
    - File handling: tools/utils/file_handlers.py
    - Validation: tools/utils/validators.py
    - New category: tools/utils/new_module.py (create __init__.py)

DEBUGGING:
==========

Enable Django debugging:
    - Set DEBUG=True in .env
    - Check error logs

Check imports:
    from tools.utils.file_handlers import validate_upload
    from tools.services import ImageProcessor
    from config.settings import IMAGE_PROCESSING
    from core.constants import MAX_IMAGE_SIZE
    from core.exceptions import ImageProcessingError

Profile code:
    from django.utils.decorators import decorator_from_middleware
    from django.middleware.common import CommonMiddleware

DOCUMENTATION:
===============

Document new functions:
    def my_function(arg1, arg2):
        \"\"\"
        Brief description.
        
        Args:
            arg1: Description
            arg2: Description
        
        Returns:
            Description of return
        
        Raises:
            ValueError: When...
        \"\"\"

DEPLOYMENT CHECKLIST:
=====================

Before deploying:
    ☐ DEBUG = False
    ☐ SECRET_KEY is strong and random
    ☐ ALLOWED_HOSTS configured
    ☐ Database migrated
    ☐ Static files collected
    ☐ Environment variables set
    ☐ Tests pass
    ☐ HTTPS enabled
    ☐ Email configured
    ☐ Backups configured

"""
