from django.shortcuts import render, redirect
from django.contrib import messages
from .reference_service import get_reference, reference_exists
from .models import SyncRequest, Prescription, Quantity, Drug
from datetime import datetime
from math import ceil

def landing(request, status = "ok"):

    return render(request, 'prescriptions/landing.html', {
        'status' : status
    })

def resume(request):

    if request.method == "POST":

        reference = request.POST.get('reference', '')
        
        syncRequest = None

        try:
            syncRequest = SyncRequest.objects.get(reference=reference)
            request.session['syncid'] = syncRequest.id
        except SyncRequest.DoesNotExist:
            return not_found_redirect()

        return redirect('prescriptions')
        

def reference(request):

    syncRequest = SyncRequest()
    syncRequest.reference = get_reference(datetime.now())
    syncRequest.save()

    return render(request, 'prescriptions/reference.html', {
        'reference' : syncRequest.reference
    })

def list_prescriptions(request):

    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']

    syncRequest = SyncRequest.objects.get(id=syncId)

    return render(request, 'prescriptions/prescriptions.html', {
        'syncRequest' : syncRequest
    })

def prescription_frequency(request, id=None):
    
    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']
    syncRequest = SyncRequest.objects.get(id=syncId)

    if id is None:
        prescription = Prescription()
    else:
        prescription = Prescription.objects.get(id=id)

        if syncRequest.id != prescription.syncRequest.id:
            return not_found_redirect()

    if request.method == "POST":

        frequency = request.POST.get('frequency', '')
        
        if frequency == '':
            messages.add_message(request, messages.WARNING, "Enter a frequency")
        else:
            try:
                frequency = int(frequency)
                if frequency > 365:
                    messages.add_message(request, messages.WARNING, "Enter a lower frequency")
                elif frequency < 1:
                    messages.add_message(request, messages.WARNING, "Enter a number greater than 0")
            except ValueError:
                messages.add_message(request, messages.WARNING, "Enter a number")

        if messages.get_messages(request):
            return render(request, 'prescriptions/frequency.html', {
                'id' : id,
                'frequency' : frequency
            })

        prescription.syncRequest = syncRequest
        prescription.frequency = frequency

        prescription.save()

        if id is None:
            return redirect('prescription', id=prescription.id)
        else:
            return redirect('prescriptions')

    frequency = ''

    if id is not None:
        frequency = prescription.frequency

    return render(request, 'prescriptions/frequency.html', {
        'id' : id,
        'frequency' : frequency
    })

def view_prescription(request, id):
    
    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    prescription = Prescription.objects.get(id=id)

    if prescription is None or prescription.syncRequest.id != request.session['syncid']:
        return not_found_redirect()
    
    return render(request, 'prescriptions/prescription.html', {
        'prescription' : prescription
    })

def item_name(request, prescriptionId, id=None):
    
    if request.session.get('syncid', None) is None:
            return timeout_redirect()

    syncId = request.session['syncid']
    
    prescription = Prescription.objects.get(id=prescriptionId)

    if prescription.syncRequest.id != syncId:
        return not_found_redirect()

    drug = None
    quantity = None

    if id is None:
        drug = Drug()
        quantity = Quantity()
    else:
        quantity = Quantity.objects.get(id=id)
        drug = quantity.drug
        if quantity not in prescription.quantity_set.all():
            return not_found_redirect()

    if request.method == "POST":

        drugName = request.POST.get('drugname', '')

        if drugName == '':
            messages.add_message(request, messages.WARNING, "Enter a drug name")

        if messages.get_messages(request):
            return render(request, 'prescriptions/itemname.html', {
                'prescriptionId' : prescriptionId,
                'id' : id,
                'drugName' : drugName
            })

        drug.name = drugName
        drug.save()

        quantity.drug = drug
        quantity.prescription = prescription
        quantity.save()

        return redirect('dosage', id=quantity.id)

    drugName = ''

    if id is not None:
        drugName = quantity.drug.name

    return render(request, 'prescriptions/itemname.html', {
        'prescriptionId' : prescriptionId,
        'id' : id,
        'drugName' : drugName
    })

def dosage(request, id):

    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']

    quantity = Quantity.objects.get(id=id)

    if quantity.prescription.syncRequest.id != syncId:
        return not_found_redirect()

    if request.method == "POST":

        dosage = None
        period = request.POST.get('period', '')

        if period == '':
            messages.add_message(request, messages.WARNING, "Choose a period")
        elif period != "1" and period != "7":
            messages.add_message(request, messages.WARNING, "Choose a valid period")
        else:
            period = int(period)

        if messages.get_messages(request):
            return render(request, 'prescriptions/dosage.html', {
                'id' : id
            })

        if period == 1:
            dosage = request.POST.get('dosage-days', '')
        else:
            dosage = request.POST.get('dosage-weeks', '')

        if dosage == '':
            messages.add_message(request, messages.WARNING, "Enter a dosage")
        else:
            try:
                dosage = int(dosage)
                if dosage > 1000:
                    messages.add_message(request, messages.WARNING, "Enter a lower dosage")
                elif dosage < 1:
                    messages.add_message(request, messages.WARNING, "Enter a dosage greater than 0")
            except ValueError:
                messages.add_message(request, messages.WARNING, "Enter a number")

        if messages.get_messages(request):
            return render(request, 'prescriptions/dosage.html', {
                'id' : id,
                'dosage' : dosage,
                'period' : period
            })

        quantity.dosage = dosage
        quantity.period = period
        quantity.perDay = dosage / period

        quantity.save()

        return redirect('stock', id=quantity.id)

    period = '' if quantity.period == -1 else quantity.period
    dosage = '' if quantity.dosage == -1 else quantity.dosage

    return render(request, 'prescriptions/dosage.html', {
        'id' : id,
        'period' : period,
        'dosage' : dosage
    })

def stock(request, id):

    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']
    
    quantity = Quantity.objects.get(id=id)

    if quantity.prescription.syncRequest.id != syncId:
        return not_found_redirect()

    if request.method == "POST":

        stock = request.POST.get('stock', '')

        if stock == '':
            messages.add_message(request, messages.WARNING, "Enter a stock")
        else:
            try:
                stock = int(stock)
                if stock > 1000:
                    messages.add_message(request, messages.WARNING, "Enter a lower stock amount")
                elif stock < 0:
                    messages.add_message(request, messages.WARNING, "Enter a value greater than or equal to 0")
            except ValueError:
                messages.add_message(request, messages.WARNING, "Enter a number")
        
        if messages.get_messages(request):
            return render(request, 'prescriptions/stock.html', {
                'id' : id,
                'stock' : stock
            })

        quantity.inStock = calculate_stock_value(quantity, stock)

        quantity.save()

        return redirect('prescription', id=quantity.prescription.id)

    stock = '' if quantity.inStock == -1 else quantity.inStock

    return render(request, 'prescriptions/stock.html', {
        'id' : id,
        'stock' : stock
    })

def check_items(request, id):

    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']

    prescription = Prescription.objects.get(id=id)

    if prescription.syncRequest.id != syncId:
        return not_found_redirect()

    if len(prescription.quantity_set.all()) == 0:
        messages.add_message(request, messages.WARNING, "Each prescription must have at least one item", "#addItem")
    else:
        for quantity in prescription.quantity_set.all():
            if quantity.inStock == -1:
                messages.add_message(request, messages.WARNING, "There is information missing from one of your items", "#editLink" + str(quantity.id))

    if messages.get_messages(request):
        return render(request, 'prescriptions/prescription.html', {
            'prescription' : prescription
        })

    return redirect('prescriptions')


def calculate(request):
    
    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']

    syncRequest = SyncRequest.objects.get(id=syncId)

    if len(syncRequest.prescription_set.all()) < 2:
        messages.add_message(request, messages.WARNING, "Add at least two prescriptions to synchronise")

    for prescription in syncRequest.prescription_set.all():
        if len(prescription.quantity_set.all()) == 0:
            messages.add_message(request, messages.WARNING, "Each prescription must have at least one item")

    if messages.get_messages(request):
        return render(request, 'prescriptions/prescriptions.html', {
            'syncRequest' : syncRequest
        })

    maximum = 0
    maxId = None

    for prescription in syncRequest.prescription_set.all():

        for quantity in prescription.quantity_set.all():

            stockInDays = quantity.inStock / quantity.perDay

            if stockInDays > maximum:
                maxId = quantity.id
                maximum = stockInDays

    for prescription in syncRequest.prescription_set.all():

        for quantity in prescription.quantity_set.all():

            if quantity.id != maxId:
                stockInDays = quantity.inStock / quantity.perDay
                requiredAmount = (maximum - stockInDays) * quantity.perDay
                roundedRequiredAmount = ceil(requiredAmount)
                quantity.required = roundedRequiredAmount
            else:
                quantity.required = 0
            quantity.save()

    return redirect('syncrequest')

def view_sync_request(request):
    
    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']

    syncRequest = SyncRequest.objects.get(id=syncId)

    return render(request, 'prescriptions/syncrequest.html', {
        'syncRequest' : syncRequest
    })

def timeout_redirect():
    return redirect('startwithstatus', status='timeout')

def not_found_redirect():
    return redirect('startwithstatus', status='notfound')

def calculate_stock_value(quantity, stock):

    maximum = quantity.prescription.frequency * quantity.perDay
    roundedMaximum = ceil(maximum)

    if stock > roundedMaximum:
        return roundedMaximum
    return stock