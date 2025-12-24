"""Home and general views."""

from django.shortcuts import render


def home(request):
    """Render home page."""
    context = {
        'title': 'Image Tools - Process Images Online',
    }
    return render(request, 'tools/home.html', context)
