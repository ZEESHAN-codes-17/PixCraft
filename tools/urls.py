from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('', views.home, name='home'),
    path('image-to-pdf/', views.image_to_pdf, name='image_to_pdf'),
    path('format-converter/', views.format_converter, name='format_converter'),
    path('image-compressor/', views.image_compressor, name='image_compressor'),
    path('qr-generator/', views.qr_generator, name='qr_generator'),
    path('image-link-generator/', views.image_link_generator, name='image_link_generator'),
    path('view-image/<str:link_id>/', views.view_shared_image, name='view_shared_image'),
    path('background-remover/', views.background_remover, name='background_remover'),
    path('id-photo-resizer/', views.id_photo_resizer, name='id_photo_resizer'),
    path('background-changer/', views.background_changer, name='background_changer'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),  # NEW: Privacy Policy
]