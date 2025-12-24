import io
import os
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from PIL import Image
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from django.utils import timezone
from datetime import timedelta
from .models import ImageLink
from django_ratelimit.decorators import ratelimit
from .security import validate_upload, sanitize_filename


def home(request):
    return render(request, 'tools/home.html')


@ratelimit(key='ip', rate='100/h', method='POST')
def image_to_pdf(request):
    if request.method == 'POST':
        # CHECK RATE LIMIT FIRST
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
        
        # Get page size option
        page_size_option = request.POST.get('page_size', 'a4')
        
        # Define page sizes
        if page_size_option == 'letter':
            page_size = letter  # 8.5" x 11"
        else:
            page_size = A4  # 210mm x 297mm (default)
        
        page_width, page_height = page_size

        # Get uploaded images
        files = request.FILES.getlist("images")
        if not files:
            return JsonResponse({'error': 'No images uploaded'}, status=400)

        pil_images = []

        try:
            for i, file in enumerate(files):
                # Validate file
                validate_upload(file, max_size_mb=10, image_only=True)
                
                img = Image.open(file)

                # Get rotation value
                rotate_val = int(request.POST.get(f"rotate_{i}", 0))
                if rotate_val != 0:
                    img = img.rotate(-rotate_val, expand=True)

                # Convert to RGB for PDF
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Handle different size options
                if page_size_option == 'original':
                    # Keep original size - no resizing
                    pil_images.append(img)
                
                elif page_size_option == 'fit-width':
                    # Fit to page width, maintain aspect ratio
                    img_width, img_height = img.size
                    aspect_ratio = img_height / img_width
                    
                    # Use 90% of page width (leave margins)
                    new_width = int(page_width * 0.9)
                    new_height = int(new_width * aspect_ratio)
                    
                    # If height exceeds page, scale down
                    if new_height > page_height * 0.9:
                        new_height = int(page_height * 0.9)
                        new_width = int(new_height / aspect_ratio)
                    
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    pil_images.append(img)
                
                else:
                    # A4 or Letter - fit to page, maintain aspect ratio
                    img_width, img_height = img.size
                    aspect_ratio = img_width / img_height
                    
                    # Calculate dimensions to fit page (with margins)
                    max_width = page_width * 0.9
                    max_height = page_height * 0.9
                    
                    if aspect_ratio > 1:
                        # Landscape image - fit to width
                        new_width = int(max_width)
                        new_height = int(new_width / aspect_ratio)
                    else:
                        # Portrait image - fit to height
                        new_height = int(max_height)
                        new_width = int(new_height * aspect_ratio)
                    
                    # Make sure it doesn't exceed page
                    if new_width > max_width:
                        new_width = int(max_width)
                        new_height = int(new_width / aspect_ratio)
                    
                    if new_height > max_height:
                        new_height = int(max_height)
                        new_width = int(new_height * aspect_ratio)
                    
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    pil_images.append(img)

            # Create PDF based on size option
            if page_size_option == 'original':
                # Original size - use PIL method (no reportlab)
                pdf_buffer = io.BytesIO()
                pil_images[0].save(
                    pdf_buffer,
                    format="PDF",
                    save_all=True,
                    append_images=pil_images[1:] if len(pil_images) > 1 else None
                )
            else:
                # A4, Letter, or Fit-width - use reportlab for consistent page sizes
                pdf_buffer = io.BytesIO()
                c = canvas.Canvas(pdf_buffer, pagesize=page_size)
                
                for img in pil_images:
                    # Convert PIL image to reportlab ImageReader
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    img_reader = ImageReader(img_buffer)
                    img_width, img_height = img.size
                    
                    # Center image on page
                    x = (page_width - img_width) / 2
                    y = (page_height - img_height) / 2
                    
                    c.drawImage(img_reader, x, y, width=img_width, height=img_height)
                    c.showPage()
                
                c.save()

            pdf_buffer.seek(0)
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="converted.pdf"'
            return response

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Processing error'}, status=500)

    return render(request, 'tools/image_to_pdf.html')


@ratelimit(key='ip', rate='100/h', method='POST')
def format_converter(request):
    """Image Format Converter - Convert between PNG, JPG, WEBP, BMP, TIFF, GIF, ICO"""
    
    if request.method == 'POST':
        # Check if rate limited
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            
        conversion_type = request.POST.get('conversion_type')
        
        if conversion_type == 'image_format':
            try:
                image_file = request.FILES.get('image')
                output_format = request.POST.get('output_format', 'PNG').upper()
                
                if not image_file:
                    return JsonResponse({'error': 'No image uploaded'}, status=400)
                
                # Validate file
                validate_upload(image_file, max_size_mb=10, image_only=True)
                
                # Open and convert image
                img = Image.open(image_file)
                
                # Handle transparency for JPG
                if output_format in ['JPEG', 'JPG'] and img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB' and output_format not in ['PNG', 'WEBP']:
                    img = img.convert('RGB')
                
                # Save to buffer
                img_buffer = io.BytesIO()
                
                if output_format == 'JPG':
                    output_format = 'JPEG'
                
                img.save(img_buffer, format=output_format, quality=95)
                img_buffer.seek(0)
                
                content_types = {
                    'PNG': 'image/png',
                    'JPEG': 'image/jpeg',
                    'WEBP': 'image/webp',
                    'BMP': 'image/bmp',
                    'TIFF': 'image/tiff',
                    'GIF': 'image/gif',
                    'ICO': 'image/x-icon'
                }
                
                response = HttpResponse(img_buffer.getvalue(), 
                                      content_type=content_types.get(output_format, 'image/png'))
                response['Content-Disposition'] = f'attachment; filename="converted.{output_format.lower()}"'
                return response
            
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'Conversion error'}, status=500)
        
        else:
            return JsonResponse({'error': 'Invalid conversion type'}, status=400)
    
    return render(request, 'tools/format_converter.html')


def image_compressor(request):
    return render(request, 'tools/image_compressor.html')


@ratelimit(key='ip', rate='100/h', method='POST')
def qr_generator(request):
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            
        link = request.POST.get('data', '').strip()
        if not link:
            return JsonResponse({'error': 'No link or text provided'}, status=400)
        
        # Limit QR code data length
        if len(link) > 2000:
            return JsonResponse({'error': 'Text too long (max 2000 characters)'}, status=400)

        size = int(request.POST.get('size', 300))
        
        # Limit size
        if size > 1000 or size < 100:
            return JsonResponse({'error': 'Invalid size (100-1000 pixels)'}, status=400)

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )
            qr.add_data(link)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            img = img.resize((size, size), Image.NEAREST)

            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            return HttpResponse(img_buffer.getvalue(), content_type='image/png')
        except Exception as e:
            return JsonResponse({'error': 'QR generation error'}, status=500)

    return render(request, 'tools/qr_generator.html')


@ratelimit(key='ip', rate='30/h', method='POST')
def image_link_generator(request):
    """Generate temporary shareable links for images"""
    
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            
        image_file = request.FILES.get('image')
        expiry_duration = request.POST.get('expiry_duration', '1d')
        
        if not image_file:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        
        try:
            # Validate file
            validate_upload(image_file, max_size_mb=5, image_only=True)
            
            # Calculate expiration time
            now = timezone.now()
            expiry_times = {
                '1h': timedelta(hours=1),
                '1d': timedelta(days=1),
                '7d': timedelta(days=7),
                '1m': timedelta(days=30),
            }
            
            expires_at = now + expiry_times.get(expiry_duration, timedelta(days=1))
            
            # Create ImageLink object
            image_link = ImageLink.objects.create(
                image=image_file,
                original_filename=sanitize_filename(image_file.name),
                expiry_duration=expiry_duration,
                expires_at=expires_at
            )
            
            # Generate shareable URL
            share_url = request.build_absolute_uri(f'/view-image/{image_link.link_id}/')
            
            return JsonResponse({
                'success': True,
                'link_id': str(image_link.link_id),
                'share_url': share_url,
                'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S'),
                'expiry_duration': expiry_duration
            })
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Error creating link'}, status=500)
    
    return render(request, 'tools/image_link_generator.html')


def view_shared_image(request, link_id):
    """View a shared image via its link"""
    
    image_link = get_object_or_404(ImageLink, link_id=link_id)
    
    if image_link.is_expired():
        image_link.delete_image_file()
        image_link.delete()
        return render(request, 'tools/link_expired.html')
    
    image_link.view_count += 1
    image_link.save()
    
    context = {
        'image_link': image_link,
        'time_remaining': image_link.expires_at - timezone.now()
    }
    
    return render(request, 'tools/view_shared_image.html', context)


@ratelimit(key='ip', rate='50/h', method='POST')
def background_remover(request):
    """Remove background from images - FREE premium feature!"""
    
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            
        image_file = request.FILES.get('image')
        
        if not image_file:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        
        try:
            # Validate file
            validate_upload(image_file, max_size_mb=10, image_only=True)
            
            from rembg import remove
            from PIL import Image
            
            img = Image.open(image_file)
            output = remove(img)
            
            img_buffer = io.BytesIO()
            output.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            response = HttpResponse(img_buffer.getvalue(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="no_background.png"'
            return response
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except ImportError:
            return JsonResponse({'error': 'Background removal library not available'}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Processing error'}, status=500)
    
    return render(request, 'tools/background_remover.html')


@ratelimit(key='ip', rate='100/h', method='POST')
def id_photo_resizer(request):
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            
        image_file = request.FILES.get('image')
        size_option = request.POST.get('size_option', '4x6')
        
        if not image_file:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        
        try:
            # Validate file
            validate_upload(image_file, max_size_mb=10, image_only=True)
            
            from PIL import Image
            
            sizes = {
                '2x2': (600, 600),
                '1x1': (300, 300),
                '4x6': (1200, 1800),
                'passport_Pakistan': (350, 450),
                'passport_us': (600, 600),
                'visa_schengen': (600, 700),
                'driving_license': (1050, 750),
            }
            
            target_size = sizes.get(size_option, (1200, 1800))
            
            img = Image.open(image_file)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]
            
            if img_ratio > target_ratio:
                new_height = target_size[1]
                new_width = int(new_height * img_ratio)
            else:
                new_width = target_size[0]
                new_height = int(new_width / img_ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            new_img = Image.new('RGB', target_size, (255, 255, 255))
            
            x_offset = (target_size[0] - new_width) // 2
            y_offset = (target_size[1] - new_height) // 2
            new_img.paste(img, (x_offset, y_offset))
            
            img_buffer = io.BytesIO()
            new_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            response = HttpResponse(img_buffer.getvalue(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="id_photo_{size_option}.png"'
            return response
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Processing error'}, status=400)
    
    return render(request, 'tools/id_photo_resizer.html')


@ratelimit(key='ip', rate='50/h', method='POST')
def background_changer(request):
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            
        image_file = request.FILES.get('image')
        mode = request.POST.get('mode', 'auto')
        bg_color_hex = request.POST.get('bg_color', '#ffffff')
        tolerance = int(request.POST.get('tolerance', 30))
        
        if not image_file:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        
        try:
            # Validate file
            validate_upload(image_file, max_size_mb=10, image_only=True)
            
            from PIL import Image
            import numpy as np
            
            bg_color_hex = bg_color_hex.lstrip('#')
            new_bg_color = tuple(int(bg_color_hex[i:i+2], 16) for i in (0, 2, 4))
            
            img = Image.open(image_file)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            
            if mode == 'auto':
                from rembg import remove
                
                img_no_bg = remove(img)
                new_img = Image.new('RGB', img_no_bg.size, new_bg_color)
                
                if img_no_bg.mode == 'RGBA':
                    new_img.paste(img_no_bg, (0, 0), img_no_bg)
                else:
                    new_img.paste(img_no_bg, (0, 0))
            
            else:
                h, w = img_array.shape[:2]
                corner_pixels = [
                    img_array[0, 0],
                    img_array[0, w-1],
                    img_array[h-1, 0],
                    img_array[h-1, w-1]
                ]
                avg_bg_color = np.mean(corner_pixels, axis=0).astype(int)
                
                color_distance = np.sqrt(np.sum((img_array.astype(int) - avg_bg_color) ** 2, axis=2))
                mask = color_distance <= tolerance
                
                new_img_array = img_array.copy()
                new_img_array[mask] = new_bg_color
                
                new_img = Image.fromarray(new_img_array.astype('uint8'))
            
            img_buffer = io.BytesIO()
            new_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            response = HttpResponse(img_buffer.getvalue(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="photo_new_background.png"'
            return response
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Processing error'}, status=400)
    
    return render(request, 'tools/background_changer.html')


@ratelimit(key='ip', rate='10/h', method='POST')
def contact(request):
    """Contact form with email confirmation"""
    
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            
        from django.core.mail import send_mail
        from django.conf import settings
        from .models import Contact
        
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            message_type = request.POST.get('message_type', 'contact')
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            attachment = request.FILES.get('attachment')
            
            # Input validation
            if not all([name, email, subject, message]):
                return JsonResponse({'error': 'Please fill in all required fields'}, status=400)
            
            # Length validation
            if len(name) > 100 or len(subject) > 200 or len(message) > 5000:
                return JsonResponse({'error': 'Input too long'}, status=400)
            
            # Validate attachment if present
            if attachment:
                validate_upload(attachment, max_size_mb=5, image_only=True)
            
            # Save to database
            contact_obj = Contact.objects.create(
                name=name,
                email=email,
                message_type=message_type,
                subject=subject,
                message=message,
                attachment=attachment
            )
            
            # Send confirmation email
            user_email_subject = f"We received your message - PixCraft"
            user_email_body = f"""
Hello {name},

Thank you for contacting PixCraft!

We have received your message and will respond within 48 hours.

Your Message Details:
-------------------
Type: {dict(Contact.MESSAGE_TYPE_CHOICES).get(message_type, 'Contact')}
Subject: {subject}

Message:
{message}

-------------------

If you have any urgent concerns, please feel free to send another message.

Best regards,
PixCraft Team

---
This is an automated confirmation email.
Reference ID: #{contact_obj.id}
            """
            
            try:
                send_mail(
                    user_email_subject,
                    user_email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as email_error:
                print(f"Email sending failed: {email_error}")
            
            return JsonResponse({
                'success': True,
                'message': 'Message sent successfully'
            })
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Error sending message'}, status=500)
    
    return render(request, 'tools/contact.html')


def privacy_policy(request):
    """Privacy Policy page"""
    return render(request, 'tools/privacy.html')