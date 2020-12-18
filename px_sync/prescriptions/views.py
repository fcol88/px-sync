"""
Main file for handling prescription sync user requests
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from prescriptions import validators
from .reference_service import get_reference
from .models import SyncRequest, Prescription, Quantity, Drug
from .calculator import calculate_stock_value, calculate_required_items

def landing(request, status = "ok"):
    """
    renders landing page - accepts status variable which has three values:
    ok - no issues with page, no error messages shown
    notfound - item not found (or unauthorised, but the user shouldn't know that)
    timeout - session has timed out
    """

    return render(request, 'prescriptions/landing.html', {
        'status' : status
    })

def resume(request):
    """
    used for both starting a new journey and resuming a journey
    loads syncid into session memory or redirects if not found
    """

    if request.method == "POST":
        reference = request.POST.get('reference', '')
        sync_request = None
        try:
            sync_request = SyncRequest.objects.get(reference=reference)
            request.session['syncid'] = sync_request.id
        except SyncRequest.DoesNotExist:

            return not_found_redirect()

        return redirect('prescriptions')

    # there is no django handler for this response but it is the correct code
    return HttpResponseNotAllowed(['POST'])

def create_sync_request(request):
    """
    creates and saves new sync request
    shows user the reference of the request should they need to return
    """

    sync_request = SyncRequest()
    sync_request.reference = get_reference(datetime.now())
    sync_request.save()

    return render(request, 'prescriptions/reference.html', {
        'reference' : sync_request.reference
    })

def list_prescriptions(request):
    """
    shows the list of prescriptions for a given sync request
    redirects if timed out
    doesn't check for DoesNotExist as it must exist to have gotten this far
    """

    sync_id = get_sync_id(request)
    if sync_id is None:

        return timeout_redirect()

    sync_request = SyncRequest.objects.get(id=sync_id)

    return render(request, 'prescriptions/prescriptions.html', {
        'syncRequest' : sync_request
    })

def frequency_form(request, prescription_id=None):
    """
    Captures the frequency of a prescription
    BOTH: if it's an existing prescription, checks to see if user is authorised
    otherwise makes a new prescription
    GET: if it's an existing prescription, populates with the old value,
    otherwise a blank string
    POST: validates that frequency is an acceptable value and rejects if not,
    otherwise it saves the prescription
    """

    sync_id = get_sync_id(request)
    if sync_id is None:

        return timeout_redirect()

    prescription = None
    if prescription_id is None:
        prescription = Prescription()
    else:
        prescription, not_found = get_prescription(prescription_id, sync_id)
        if not_found:

            return not_found_redirect()

    if request.method == "POST":
        frequency = validators.validate_frequency(request)
        if messages.get_messages(request):

            return render(request, 'prescriptions/frequency.html', {
                'id' : prescription_id,
                'frequency' : frequency
            })

        sync_request = SyncRequest.objects.get(id=sync_id)
        prescription.syncRequest = sync_request
        prescription.frequency = frequency
        prescription.save()

        if prescription_id is None:

            return redirect('prescription', prescription_id=prescription.id)

        return redirect('prescriptions')

    frequency = ''
    if prescription_id is not None:
        frequency = prescription.frequency

    return render(request, 'prescriptions/frequency.html', {
        'id' : prescription_id,
        'frequency' : frequency
    })

def view_prescription(request, prescription_id):
    """
    Shows the details of a given prescription
    Redirects if unauthorised or invalid
    """

    sync_id = get_sync_id(request)

    if sync_id is None:

        return timeout_redirect()

    prescription = None
    prescription, not_found = get_prescription(prescription_id, sync_id)
    if not_found:

        return not_found_redirect()

    return render(request, 'prescriptions/prescription.html', {
        'prescription' : prescription
    })

def item_name_form(request, prescription_id, quantity_id=None):
    """
    Captures drug name of prescription item
    BOTH: if it's an existing item, checks to see if user is authorised
    GET: if it's an existing item, populates the field with the name
    POST: validates that it's an acceptable name, then saves both drug
    and quantity (the latter to instantiate if new)
    """

    sync_id = get_sync_id(request)
    if sync_id is None:

        return timeout_redirect()

    prescription, not_found = get_prescription(prescription_id, sync_id)
    drug = None
    quantity = None
    if quantity_id is None:
        drug = Drug()
        quantity = Quantity()
    elif not not_found:
        quantity, not_found = get_quantity(quantity_id, sync_id)
        drug = None if not_found else quantity.drug
    if not_found:

        return not_found_redirect()

    if request.method == "POST":
        drug_name = validators.validate_drug_name(request)
        if messages.get_messages(request):

            return render(request, 'prescriptions/itemname.html', {
                'prescriptionId' : prescription_id,
                'id' : quantity_id,
                'drugName' : drug_name
            })

        drug.name = drug_name
        drug.save()
        quantity.drug = drug
        quantity.prescription = prescription
        quantity.save()

        return redirect('dosage', quantity_id=quantity.id)

    drug_name = ''

    if quantity_id is not None:
        drug_name = quantity.drug.name

    return render(request, 'prescriptions/itemname.html', {
        'prescriptionId' : prescription_id,
        'id' : quantity_id,
        'drugName' : drug_name
    })

def dosage_form(request, quantity_id):
    """
    Captures dosage and period information
    BOTH: is an existing item at this point - checks if the user is authorised
    GET: populates period and dosage (blank if it hasn't been filled in yet)
    POST: checks for valid values and rejects if they're not,
    then saves both and a third, computed field to make calculation
    easier later on
    """

    sync_id = get_sync_id(request)
    if sync_id is None:

        return timeout_redirect()

    quantity, not_found = get_quantity(quantity_id, sync_id)
    if not_found:

        return not_found_redirect()

    if request.method == "POST":
        period = validators.validate_period(request)
        if messages.get_messages(request):

            return render(request, 'prescriptions/dosage.html', {
                'id' : quantity_id
            })

        dosage = validators.validate_dosage(request, period)
        if messages.get_messages(request):

            return render(request, 'prescriptions/dosage.html', {
                'id' : quantity_id,
                'dosage' : dosage,
                'period' : period
            })

        quantity.dosage = dosage
        quantity.period = period
        quantity.perDay = dosage / period
        quantity.save()

        return redirect('stock', quantity_id=quantity.id)

    period = '' if quantity.period == -1 else quantity.period
    dosage = '' if quantity.dosage == -1 else quantity.dosage

    return render(request, 'prescriptions/dosage.html', {
        'id' : quantity_id,
        'period' : period,
        'dosage' : dosage
    })

def stock_form(request, quantity_id):
    """
    Captures stock information about prescription item
    BOTH: is an existing item at this point - checks if user is authorised
    GET: populates existing data (blank if it hasn't been filled in yet)
    POST: checks for a valid value and rejects if not, then saves a
    computed value
    """

    sync_id = get_sync_id(request)
    if sync_id is None:

        return timeout_redirect()

    quantity, not_found = get_quantity(quantity_id, sync_id)
    if not_found:

        return not_found_redirect()

    if request.method == "POST":
        stock = validators.validate_stock(request)
        if messages.get_messages(request):

            return render(request, 'prescriptions/stock.html', {
                'id' : quantity_id,
                'stock' : stock
            })

        quantity.inStock, quantity.rawStock = calculate_stock_value(quantity, stock)
        quantity.save()

        return redirect('prescription', prescription_id=quantity.prescription.id)

    stock = '' if quantity.inStock == -1 else quantity.inStock

    return render(request, 'prescriptions/stock.html', {
        'id' : quantity_id,
        'stock' : stock
    })

def check_items(request, prescription_id):
    """
    Validates that all prescription items are complete before
    redirecting to the prescription list view
    """

    sync_id = get_sync_id(request)
    if sync_id is None:

        return timeout_redirect()

    prescription, not_found = get_prescription(prescription_id, sync_id)
    if not_found:

        return not_found_redirect()

    validators.validate_prescription_items(request, prescription)
    if messages.get_messages(request):

        return render(request, 'prescriptions/prescription.html', {
            'prescription' : prescription
        })

    return redirect('prescriptions')

def calculate(request):
    """
    Calculates the required amounts for the prescription synchronisation
    request, then redirects to a page showing the required amounts
    """

    sync_id = get_sync_id(request)

    if sync_id is None:

        return timeout_redirect()

    sync_request = validators.validate_sync_request(request, sync_id)
    if messages.get_messages(request):

        return render(request, 'prescriptions/prescriptions.html', {
            'syncRequest' : sync_request
        })

    calculate_required_items(sync_request)

    return redirect('syncrequest')

def view_sync_request(request):
    """
    Shows the completed sync request
    """

    sync_id = get_sync_id(request)
    if sync_id is None:

        return timeout_redirect()

    sync_request = SyncRequest.objects.get(id=sync_id)

    return render(request, 'prescriptions/syncrequest.html', {
        'syncRequest' : sync_request
    })

def timeout_redirect():
    """
    redirects to the landing page with a status of timeout
    """

    return redirect('startwithstatus', status='timeout')

def not_found_redirect():
    """
    redirects to the landing page with a status of notfound
    """

    return redirect('startwithstatus', status='notfound')

def get_sync_id(request):
    """
    gets the current sync id, or returns None if not present
    """

    return request.session.get('syncid', None)

def get_prescription(prescription_id, sync_id):
    """
    tries to get a prescription from the database
    if it can't find it, returns none and not_found=True,
    otherwise it checks if the prescription matches the details expected
    if the user isn't authorised, acts as if it hasn't been found
    """

    prescription = None
    not_found = False
    try:
        prescription = Prescription.objects.get(id=prescription_id)
        if prescription.syncRequest.id != sync_id:
            not_found = True
    except Prescription.DoesNotExist:
        not_found = True

    return prescription, not_found

def get_quantity(quantity_id, sync_id):
    """
    tries to get a quantity from the database
    if it can't find it, returns none and not_found=True,
    otherwise it checks if the prescription matches the details expected
    if the user isn't authorised, acts as if it hasn't been found
    """

    quantity = None
    not_found = False
    try:
        quantity = Quantity.objects.get(id=quantity_id)
        if quantity.prescription.syncRequest.id != sync_id:
            not_found = True
    except Quantity.DoesNotExist:
        not_found = True

    return quantity, not_found
