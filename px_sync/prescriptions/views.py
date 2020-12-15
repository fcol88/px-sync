from django.shortcuts import render, redirect
from django.contrib import messages
from .reference_service import get_reference, reference_exists
from .models import SyncRequest, Prescription, Quantity, Drug
from datetime import datetime

def landing(request, status = "ok"):

    request.session.set_expiry(60)

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

    if request.method == "POST":

        frequency = request.POST.get('frequency', '')
        
        if frequency is None:
            messages.add_message(request, messages.WARNING, "Enter a frequency")
            return render(request, 'prescriptions/frequency.html')
        else:
            try:
                frequency = int(frequency)
                if frequency > 365:
                    messages.add_message(request, messages.WARNING, "Enter a lower frequency")
            except ValueError:
                messages.add_message(request, messages.WARNING, "Enter a number")
                return render(request, 'prescriptions/frequency.html')

        if messages:
            return render(request, 'prescriptions/frequency.html')

        syncId = request.session['syncid']
        syncRequest = SyncRequest.objects.get(id=syncId)

        prescription = None

        if id is None:
            prescription = Prescription()
        else:
            prescription = Prescription.objects.get(id=id)

            if syncRequest.id != prescription.syncRequest.id:
                return not_found_redirect()

        prescription.syncRequest = syncRequest
        prescription.frequency = frequency

        prescription.save()

        return redirect('prescription', id=prescription.id)

    return render(request, 'prescriptions/frequency.html')

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

    if request.method == "POST":

        drugName = request.POST.get('drugname', '')

        if drugName is None:
            messages.add_message(request, messages.WARNING, "Enter a drug name")
            return render(request, 'prescriptions/drugname.html')

        syncId = request.session['syncid']

        prescription = Prescription.objects.get(id=prescriptionId)

        if prescription.syncRequest.id != syncId:
            return not_found_redirect()

        drug = None

        if id is None:
            drug = Drug()
        else:
            quantity = Quantity.objects.get(id=id)
            drug = quantity.drug

        drug.name = drugName

        drug.save()

        return redirect('dosage', prescriptionId=prescriptionId, drugId=drug.id, id=id)

    return render(request, 'prescriptions/itemname.html')

def dosage(request, prescriptionId, drugId, id=None):

    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    if request.method == "POST":

        dosage = request.POST.get('dosage', '')
        period = request.POST.get('period', '')

        if period is None:
            messages.add_message(request, messages.WARNING, "Choose a period")
        elif period != 1 and period != 7:
            messages.add_message(request, messages.WARNING, "Choose a valid period")

        if dosage is None:
            messages.add_message(request, messages.WARNING, "Enter a dosage")
        else:
            try:
                dosage = int(dosage)
                if dosage > 1000:
                    messages.add_message(request, messages.WARNING, "Enter a lower dosage")
            except ValueError:
                messages.add_message(request, messages.WARNING, "Enter a number")

        if messages:
            return render(request, 'prescriptions/dosage.html')

        syncId = request.session['syncid']
        
        prescription = Prescription.objects.get(id=prescriptionId)

        if prescription.syncRequest.id != syncId:
            return not_found_redirect()

        quantity = None

        if id is None:
            quantity = Quantity()
        else:
            quantity = Quantity.objects.get(id=id)

        quantity.prescribed = dosage * period
        quantity.drug = Drug.objects.get(id=drugId)

        quantity.save()

        return redirect('stock', id=quantity.id)

    return render(request, 'prescriptions/dosage.html')

def stock(request, id):

    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    if request.method == "POST":

        stock = request.POST.get('stock', '')

        if stock is None:
            messages.add_message(request, messages.WARNING, "Enter a stock")
        else:
            try:
                stock = int(stock)
            except ValueError:
                messages.add_message(request, messages.WARNING, "Enter a number")
        
        if messages:
            return render(request, 'prescriptions/stock.html')

        syncId = request.session['syncid']

        quantity = Quantity.objects.get(id=id)

        if quantity.prescription.syncRequest.id != syncId or quantity is None:
            return not_found_redirect()

        quantity.stock = calculate_stock_value(quantity, stock)

        quantity.save()

        return redirect('prescription', id=quantity.prescription.id)

    return render(request, 'prescriptions/stock.html')

def check_items(request, id):

    if request.session.get('syncid', None) is None:
        return timeout_redirect()

    syncId = request.session['syncid']

    prescription = Prescription.objects.get(id=id)

    if prescription.syncRequest.id != syncId:
        return not_found_redirect()

    if len(prescription.quantity_set.all) == 0:
        messages.add_message(request, messages.WARNING, "Each prescription must have at least one item")

    if messages:
        return render(request, 'prescriptions/prescription.html', {
            'prescription' : prescription
        })

    return redirect('prescriptions')


def calculate(request):
    pass

def timeout_redirect():
    return redirect('startwithstatus', status='timeout')

def not_found_redirect():
    return redirect('startwithstatus', status='notfound')

def calculate_stock_value(quantity, stock):

    maximum = quantity.prescription.frequency * quantity.prescribed

    if stock > maximum:
        return maximum
    return stock