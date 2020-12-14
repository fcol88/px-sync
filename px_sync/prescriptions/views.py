from django.shortcuts import render, redirect
from .reference_service import get_reference, reference_exists
from .models import SyncRequest
from datetime import datetime

def landing(request, found = "found"):

    return render(request, 'prescriptions/landing.html', {
        'found' : found
    })

def resume(request):

    if request.method == "POST":

        reference = request.POST.get('reference', '')
        request.session['reference'] = reference
        return redirect('prescriptions')
        

def reference(request):

    syncRequest = SyncRequest()
    syncRequest.reference = get_reference(datetime.now())
    syncRequest.save()

    return render(request, 'prescriptions/reference.html', {
        'reference' : syncRequest.reference
    })

def prescriptions(request): 
    
    reference = get_reference_or_redirect_if_none(request)

    syncRequest = None

    try:
        syncRequest = SyncRequest.objects.get(reference=reference)
    except SyncRequest.DoesNotExist:
        return redirect('notfound', found='notfound')

    return render(request, 'prescriptions/prescriptions.html', {
        'syncRequest' : syncRequest
    })

def viewprescription(request):
    pass

def frequency(request):
    pass

def calculate(request):
    pass

def get_reference_or_redirect_if_none(request):

    reference = request.session['reference']

    if reference is None:
        return redirect('notfound', found='notfound')

    return reference