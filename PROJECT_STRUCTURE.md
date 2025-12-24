# IMAGE TOOLS PROJECT - COMPLETE STRUCTURE (Latest Update - Dec 24, 2025)

```
image_tools_project/
│
├── 📄 manage.py                 # Django management script
├── 📄 db.sqlite3                # SQLite database
├── 📄 .env                      # Environment variables (NEVER commit!)
├── 📄 .env.example              # Example environment file
├── 📄 .gitignore                # Git ignore rules
│
├── 📚 PROJECT DOCUMENTATION
├── 📄 README.md                 # Main project documentation
├── 📄 CONTRIBUTING.md           # Development guidelines
├── 📄 STRUCTURE.md              # Architecture overview
├── 📄 PROJECT_STRUCTURE.md      # Complete project structure (this file)
├── 📄 REQUIREMENTS.md           # Requirements management guide
│
├── 🔧 MAIN PROJECT CONFIG
├── 📁 image_tools_project/
│   ├── __init__.py
│   ├── 📄 settings.py           # Main Django settings
│   ├── 📄 urls.py               # Root URL routing
│   ├── 📄 wsgi.py               # WSGI configuration
│   ├── 📄 asgi.py               # ASGI configuration
│   ├── 📄 requirements.txt       # Project dependencies
│   ├── __pycache__/
│   └── static/
│       ├── css/
│       │   └── style.css        # Main stylesheet
│       ├── fonts/               # Font files
│       └── js/
│           └── script.js        # Main JavaScript
│
├── 📦 CORE UTILITIES
├── 📁 core/
│   ├── __init__.py
│   ├── 📄 constants.py          # App-wide constants
│   └── 📄 exceptions.py         # Custom exception classes
│
├── ⚙️ APP CONFIGURATION
├── 📁 config/
│   ├── __init__.py
│   └── 📄 settings.py           # Centralized app settings
│
├── 💾 MEDIA FILES
├── 📁 media/
│   ├── contact_attachments/     # Contact form attachments
│   └── temp_images/             # Temporary image storage
│
├── 🎯 MAIN DJANGO APP
├── 📁 tools/
│   │
│   ├── 📄 models.py             # Database models
│   ├── 📄 views.py              # Main view handlers
│   ├── 📄 urls.py               # App URL routing
│   ├── 📄 admin.py              # Django admin configuration
│   ├── 📄 apps.py               # App configuration
│   ├── 📄 security.py           # Security utilities
│   ├── 📄 tests.py              # Additional tests
│   │
│   ├── 🛠️ UTILITIES & HELPERS
│   ├── 📁 utils/
│   │   ├── __init__.py
│   │   ├── 📄 file_handlers.py  # File upload validation & handling
│   │   └── 📄 validators.py     # Input validation helpers
│   │
│   ├── 💼 BUSINESS LOGIC SERVICES
│   ├── 📁 services/
│   │   ├── __init__.py
│   │   └── 📄 image_processor.py # Core image processing service
│   │
│   ├── 📋 FORMS & VALIDATION
│   ├── 📁 forms/
│   │   ├── __init__.py
│   │   └── 📄 image_forms.py    # Image processing forms
│   │
│   ├── 👁️ MODULAR VIEWS
│   ├── 📁 views_modules/
│   │   ├── __init__.py
│   │   └── 📄 home_views.py     # Home page views
│   │
│   ├── 🧪 TEST SUITE
│   ├── 📁 tests/
│   │   ├── __init__.py
│   │   └── 📄 test_image_processor.py
│   │
│   ├── 🎨 HTML TEMPLATES
│   ├── 📁 templates/
│   │   └── tools/
│   │       ├── 📄 base.html                # Base template
│   │       ├── 📄 home.html                # Home page
│   │       ├── 📄 image_to_pdf.html        # Image to PDF converter
│   │       ├── 📄 format_converter.html    # Format converter
│   │       ├── 📄 image_compressor.html    # Image compression tool
│   │       ├── 📄 qr_generator.html        # QR code generator
│   │       ├── 📄 image_link_generator.html # Generate shareable links
│   │       ├── 📄 view_shared_image.html   # View shared images
│   │       ├── 📄 background_remover.html  # Remove image background
│   │       ├── 📄 background_changer.html  # Change image background
│   │       ├── 📄 id_photo_resizer.html    # Resize ID photos
│   │       ├── 📄 contact.html             # Contact form
│   │       ├── 📄 link_expired.html        # Expired link notice
│   │       └── 📄 privacy.html             # Privacy policy
│   │
│   └── 📁 migrations/
│       ├── __init__.py
│       ├── 📄 0001_initial.py
│       ├── 📄 0002_contact.py
│       ├── 📄 0003_alter_imagelink_image.py
│       └── __pycache__/
│
└── 🌐 VIRTUAL ENVIRONMENT
    └── 📁 venv/                 # Python virtual environment (not committed)

```

## Features by Module

### Home Page
- **File**: `home_views.py` - Homepage display
- **Template**: `home.html`

### Image Processing
- **Converter**: Format conversion between image types
- **Compressor**: Image compression utility
- **Background Remover**: Remove backgrounds from images
- **Background Changer**: Change image backgrounds
- **ID Photo Resizer**: Resize photos for ID purposes

### Additional Tools
- **QR Generator**: Generate QR codes from URLs/text
- **Image to PDF**: Convert images to PDF documents
- **Link Generator**: Create shareable links for images
- **View Shared Images**: Display shared image content
- **Contact Form**: User contact and feedback form

## Architecture Layers

1. **Views** (`views.py`, `views_modules/`) - HTTP request handling
2. **Forms** (`forms/`) - Django form definitions and validation
3. **Services** (`services/`) - Business logic and core functionality
4. **Models** (`models.py`) - Database schema and ORM
5. **Utilities** (`utils/`) - Helper functions and common operations
6. **Configuration** (`config/`, `core/`) - Settings and constants

## Key Files Summary

| Component | File | Purpose |
|-----------|------|---------|
| **Django Config** | `image_tools_project/settings.py` | Main Django configuration |
| **URL Routing** | `image_tools_project/urls.py` | Root URL patterns |
| **App Config** | `config/settings.py` | App-specific settings |
| **Constants** | `core/constants.py` | Application-wide constants |
| **Exceptions** | `core/exceptions.py` | Custom exception classes |
| **Models** | `tools/models.py` | Database models |
| **Views** | `tools/views.py` | Main view handlers |
| **Forms** | `tools/forms/image_forms.py` | Form definitions |
| **Services** | `tools/services/image_processor.py` | Business logic |
| **Utils** | `tools/utils/` | Helper functions |
| **Templates** | `tools/templates/tools/` | HTML templates |
| **Static Files** | `image_tools_project/static/` | CSS, JS, fonts |
| **Media Files** | `media/` | User uploads and temp files |
