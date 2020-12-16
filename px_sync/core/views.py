from django.shortcuts import render

def page_not_found(request, exception):
    return render(request, '404.html')

def server_error(request):
    return render(request, '500.html')