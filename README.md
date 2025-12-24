# PixCraft - Professional Image Processing Platform

[![License: Custom](https://img.shields.io/badge/License-Custom-blue.svg)](LICENSE)
[![Made with Django](https://img.shields.io/badge/Made%20with-Django-092E20?logo=django)](https://www.djangoproject.com/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Status: Active](https://img.shields.io/badge/Status-Active%20Development-success)](https://github.com/yourusername/pixcraft)

**🎨 Free Image Processing Tools - Background Removal, PDF Conversion, QR Generation & More**

> **Note**: This project is open for learning and inspiration, but please read the [License](#-license--usage-terms) before using.

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Security](#-security)
- [Deployment](#-deployment)
- [License & Usage](#-license--usage-terms)
- [Contributing](#-contributing)
- [Support](#-support--contact)

---

## ✨ Features

### 🖼️ Image Processing Tools
- **Format Converter** - Convert between PNG, JPG, WEBP, BMP, TIFF, GIF
- **Image Compressor** - Reduce file size while maintaining quality
- **Background Remover** - AI-powered background removal (FREE Premium!)
- **Background Changer** - Replace backgrounds with custom colors
- **ID Photo Resizer** - Resize for passports, visas, licenses
- **Image to PDF** - Convert multiple images with size options (A4, Letter, Fit-Width, Original)

### 🔧 Additional Tools
- **QR Code Generator** - Generate custom-sized QR codes from text/URLs
- **Image Link Generator** - Create secure, temporary shareable links (1h - 1 month)
- **Shared Image Viewer** - View shared images with expiration tracking

### 📧 User Features
- **Contact/Complaint Center** - User feedback system with email confirmation
- **Privacy Policy** - Comprehensive privacy protection with encrypted storage
- **Rate Limiting** - Protection against abuse (50-100 requests/hour)

### 🎯 Advanced Features
- **Drag & Drop Upload** - Intuitive file upload interface
- **Image Rotation** - Rotate images before processing (90°, 180°, 270°)
- **Image Reordering** - Drag to reorder multiple images
- **Encrypted Filenames** - SHA256 encrypted storage for privacy
- **Auto-Expiration** - Temporary files automatically deleted

---

## 📸 Screenshots

> Add screenshots here when deploying!

---

## 🛠️ Tech Stack

### Backend
- **Django 5.2.8** - Web framework
- **Python 3.8+** - Programming language
- **SQLite** - Database (dev) / PostgreSQL (production)

### Image Processing
- **Pillow 11.3.0** - Image manipulation
- **ReportLab 4.4.5** - PDF generation
- **Rembg 2.0.69** - AI background removal
- **OpenCV** - Advanced image processing
- **qrcode 8.2** - QR code generation

### Security & Utilities
- **django-ratelimit** - Rate limiting
- **python-decouple** - Environment variables
- **python-docx** - Document processing

### Frontend
- **Bootstrap 5.3.2** - UI framework
- **Font Awesome 6.4.2** - Icons
- **Vanilla JavaScript** - Interactive features

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git
- Virtual environment (recommended)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/pixcraft.git
cd pixcraft

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your settings

# 6. Run migrations
python manage.py migrate

# 7. Create superuser (optional)
python manage.py createsuperuser

# 8. Start development server
python manage.py runserver

# 9. Open in browser
# http://localhost:8000/
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here-generate-new-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=noreply@pixcraft.com

# Database (Optional - for PostgreSQL)
# DATABASE_URL=postgresql://user:pass@localhost:5432/pixcraft_db

# AWS S3 (Optional - for production)
# USE_S3=False
# AWS_ACCESS_KEY_ID=your-key
# AWS_SECRET_ACCESS_KEY=your-secret
# AWS_STORAGE_BUCKET_NAME=your-bucket
```

**Important**: 
- Generate new `SECRET_KEY` using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Use Gmail **App Password**, not your regular password
- Set `DEBUG=False` in production

### File Upload Limits
- Max file size: **10 MB** (configurable)
- Allowed formats: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP
- Temporary files expire: **24 hours**

---

## 💻 Usage

### Web Interface
Access all tools at `http://localhost:8000/`

### Admin Panel
Manage submissions at `http://localhost:8000/admin/`
- View contact messages
- Manage shared image links
- Monitor usage statistics

---

## 🔌 API Endpoints

| Feature | Endpoint | Method | Rate Limit |
|---------|----------|--------|------------|
| Home | `/` | GET | - |
| Image to PDF | `/image-to-pdf/` | POST | 100/hour |
| Format Converter | `/format-converter/` | POST | 100/hour |
| QR Generator | `/qr-generator/` | POST | 100/hour |
| Background Remover | `/background-remover/` | POST | 50/hour |
| Background Changer | `/background-changer/` | POST | 50/hour |
| Link Generator | `/image-link-generator/` | POST | 30/hour |
| View Shared Image | `/view-image/<link_id>/` | GET | - |
| Contact Form | `/contact/` | POST | 10/hour |
| Privacy Policy | `/privacy/` | GET | - |

---

## 🔒 Security

### Implemented Security Features

✅ **CSRF Protection** - All forms protected  
✅ **SQL Injection Prevention** - Django ORM parameterized queries  
✅ **XSS Prevention** - Template auto-escaping  
✅ **Rate Limiting** - Prevent abuse and DoS attacks  
✅ **File Validation** - Type checking, size limits  
✅ **Encrypted Storage** - SHA256 hashed filenames  
✅ **Input Sanitization** - Filename and data validation  
✅ **Secure Headers** - CSRF tokens, secure cookies  
✅ **Auto-Deletion** - Temporary files expire automatically  

### Production Security Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure AWS S3 for media
- [ ] Set up error monitoring (Sentry)
- [ ] Enable security headers
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up regular backups

---

## 🚢 Deployment

### Deploy to Railway (Recommended)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Add PostgreSQL
railway add

# 5. Set environment variables
railway variables set SECRET_KEY=your-key
railway variables set DEBUG=False
railway variables set EMAIL_HOST_USER=your-email
railway variables set EMAIL_HOST_PASSWORD=your-password

# 6. Deploy
railway up
```

### Deploy with Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start
CMD ["sh", "-c", "python manage.py migrate && gunicorn image_tools_project.wsgi:application --bind 0.0.0.0:8000"]
```

```bash
docker build -t pixcraft .
docker run -p 8000:8000 --env-file .env pixcraft
```

---

## 📄 License & Usage Terms

**Copyright © 2025 Zeeshan Ali. All Rights Reserved.**

### ✅ What You CAN Do:
- 📖 Learn from the code and study the architecture
- 💡 Use code snippets in your own projects
- 🎓 Use for educational purposes
- 🛠️ Build your own unique image processing tool (with different branding)
- 🌟 Fork and modify for personal/portfolio projects

### ❌ What You CANNOT Do:
- 🚫 Deploy an identical copy of PixCraft as a competing service
- 🚫 Use the "PixCraft" name, logo, or branding
- 🚫 Create a competing service without substantial modifications
- 🚫 Copy the exact UI, design, or feature set without changes
- 🚫 Remove copyright notices or author attribution

### 🎨 If You Want To Build Your Own Version:

**You MUST:**
1. ✅ Create your own unique brand name (not "PixCraft")
2. ✅ Design your own UI/UX (different colors, layout, components)
3. ✅ Add your own creative features and improvements
4. ✅ Credit the original: *"Inspired by PixCraft by Zeeshan Ali"*
5. ✅ Make it YOUR project with YOUR creativity

### 💡 Examples:

**❌ NOT ALLOWED:**
- Clone repo → Deploy as "PixCraft Clone" → Same features/design

**✅ ALLOWED:**
- Clone repo → Study code → Build "ImageMagic" with unique UI → Add new features → Deploy

### 🏆 Competition Welcome!

Want to build a competing image processing tool? **Great!** 

**Please:**
- ✅ Study my code and learn the techniques
- ✅ Build YOUR version with YOUR unique vision
- ✅ Add YOUR innovative features
- ✅ Use YOUR own branding and identity
- ✅ Credit the inspiration: "Based on concepts from PixCraft"
- ✅ Make it BETTER than mine (I love healthy competition! 💪)

**Don't:**
- ❌ Copy-paste and deploy an identical clone
- ❌ Steal my branding or pretend it's your original work
- ❌ Deploy without adding your creative touch

### 📧 Questions About Usage?

Contact: zeeshanali4k2517@gmail.com

**Remember**: This project represents months of learning and hard work. 
If you use it, please respect the effort by giving credit and adding your own creativity. 
Let's build amazing things together! 🚀

---

**TL;DR**: 
- Learn from it? ✅ YES  
- Use snippets? ✅ YES  
- Build your own version? ✅ YES  
- Deploy identical clone? ❌ NO  
- Steal branding? ❌ NO  

See [LICENSE](LICENSE) for full legal terms.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes** (follow PEP 8, add tests, update docs)
4. **Test thoroughly** (`python manage.py test`)
5. **Commit** (`git commit -m 'Add AmazingFeature'`)
6. **Push** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

### Contribution Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive
- Be respectful and constructive

---

## 💬 Support & Contact

### 🐛 Found a Bug?
- Open an issue: [GitHub Issues](../../issues)
- Include: Steps to reproduce, expected vs actual behavior, screenshots

### 💡 Feature Request?
- Open a feature request with detailed description
- Explain the use case and benefits

### 📧 Contact
- **Email**: zeeshanali4k2517@gmail.com
- **GitHub**: [@yourusername](https://github.com/yourusername)

### ⭐ Show Your Support
- Star this repository if you find it useful
- Share with others who might benefit
- Follow for updates

---

## 📊 Project Stats

- **Language**: Python 3.8+
- **Framework**: Django 5.2.8
- **Lines of Code**: 2000+
- **Templates**: 14 HTML files
- **Features**: 10+ tools
- **Dependencies**: 50+ packages
- **Test Coverage**: Growing

---

## 🗺️ Roadmap

### Version 1.0.0 ✅ (Current)
- ✅ Core image processing tools
- ✅ Background removal (AI-powered)
- ✅ PDF conversion with size options
- ✅ Encrypted file storage
- ✅ Rate limiting & security
- ✅ Contact form system
- ✅ Privacy policy

### Version 1.1.0 🚧 (Planned)
- [ ] User authentication & accounts
- [ ] Saved preferences & history
- [ ] Batch processing
- [ ] API endpoints for developers
- [ ] Premium features integration

### Version 2.0.0 💭 (Future)
- [ ] Advanced AI filters
- [ ] Mobile app (React Native)
- [ ] OCR text extraction
- [ ] Payment integration
- [ ] Analytics dashboard

---

## 🙏 Acknowledgments

- **Django** - Amazing web framework
- **Rembg** - AI background removal
- **Bootstrap** - Beautiful UI components
- **Community** - Thanks to all contributors!

---

## 📜 Changelog

### v1.0.0 (December 24, 2025)
- 🎉 Initial public release
- ✅ 10+ image processing features
- ✅ Complete security implementation
- ✅ Encrypted file storage
- ✅ Rate limiting
- ✅ Privacy policy
- ✅ Contact system

---

<div align="center">

**Made with ❤️ by [Zeeshan Ali](https://github.com/yourusername)**

⭐ Star this repo if you find it helpful!

[Report Bug](../../issues) · [Request Feature](../../issues) · [Documentation](../../wiki)

</div>

---

**Last Updated**: December 24, 2025  
**Version**: 1.0.0  
**Status**: ✅ Active Development  
**License**: Custom (See LICENSE file)