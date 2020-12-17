"""
views file for common components
"""

from django.shortcuts import render

def page_not_found(request, exception):
    """
    Renders page not found page
    """
    return render(request, '404.html')

def server_error(request):
    """
    Renders internal server error page
    """
    return render(request, '500.html')