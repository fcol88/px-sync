"""
Prescriber application views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from prescriptions.models import SyncRequest, Quantity

def login_page(request):
    """
    renders login page, accepts post request and logs user in if valid
    """

    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('search')

        messages.add_message(request, messages.WARNING,
        "Username or password is incorrect")

    return render(request, 'prescriber/login.html')

def logout_page(request):
    """
    logs out user and redirects to login form
    """
    logout(request)

    return redirect('login')

@login_required(login_url="/prescriber/login")
def request_search(request):
    """
    Handles search form requests
    GET: renders search page
    POST: looks for exact reference match - if nothing found, shows error,
    otherwise redirects to view
    """

    if request.method == "POST":
        search_term = request.POST.get('search', '')
        sync_request = None
        try:
            sync_request = SyncRequest.objects.get(reference=search_term)
        except SyncRequest.DoesNotExist:
            messages.add_message(request, messages.WARNING,
            "Sync request not found")
            return render(request, 'prescriber/search.html', {
                'search' : search_term
            })

        return redirect('viewrequest', sync_id=sync_request.id)

    return render(request, 'prescriber/search.html')

@login_required(login_url="/prescriber/login")
def view_request(request, sync_id):
    """
    renders synchronisation view
    """

    sync_request = SyncRequest.objects.get(id=sync_id)

    # get a list of items with non-zero required amounts
    # used to check if a table is needed
    sync_table_required = Quantity.objects.filter(
        prescription__in=sync_request.prescription_set.all()).filter(
            required__gt=0)

    return render(request, 'prescriber/view.html', {
        'syncRequest' : sync_request,
        'syncTableRequired' : sync_table_required
    })
