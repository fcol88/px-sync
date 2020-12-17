"""
Validators to assess whether user input is within accepted parameters
"""

from django.contrib import messages
from .models import SyncRequest

def validate_frequency(request):
    """
    Validates prescription frequency.
    Accepted parameters are:
    -Must be a number
    -Must be less than 365 (may change based on user feedback)
    -Must be greater than 0
    """

    frequency = request.POST.get('frequency', '')
    if frequency == '':
        messages.add_message(request, messages.WARNING, "Enter a frequency")
    else:
        try:
            frequency = int(frequency)
            if frequency > 365:
                messages.add_message(request, messages.WARNING,
                "Enter a lower frequency")
            elif frequency < 1:
                messages.add_message(request, messages.WARNING,
                "Enter a number greater than 0")
        except ValueError:
            messages.add_message(request, messages.WARNING, "Enter a number")

    return frequency

def validate_drug_name(request):
    """
    Validates drug name.
    Accepted parameters are:
    -Not blank
    """

    drug_name = request.POST.get('drugname', '')
    if drug_name == '':
        messages.add_message(request, messages.WARNING, "Enter a drug name")

    return drug_name

def validate_period(request):
    """
    Validates dose period.
    Accepted parameters are:
    -1
    -7
    """

    period = request.POST.get('period', '')
    if period == '':
        messages.add_message(request, messages.WARNING, "Choose a period")
    elif period not in ('1', '7'):
        messages.add_message(request, messages.WARNING,
        "Choose a valid period")
    else:
        period = int(period)

    return period

def validate_dosage(request, period):
    """
    Validates dosage.
    Accepts period as a parameter to decide which form field to get
    Accepted parameters are:
    -Must be a number
    -Must be less than 1001 (may change based on user feedback)
    -Must be greater than zero
    """

    dosage = None
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
                messages.add_message(request, messages.WARNING,
                "Enter a lower dosage")
            elif dosage < 1:
                messages.add_message(request, messages.WARNING,
                "Enter a dosage greater than 0")
        except ValueError:
            messages.add_message(request, messages.WARNING, "Enter a number")

    return dosage

def validate_stock(request):
    """
    Validates stock levels.
    Accepted parameters are:
    -Must be a number
    -Must be less than 1000 (may change based on user feedback)
    -Must be greater than or equal to 0
    """

    stock = request.POST.get('stock', '')
    if stock == '':
        messages.add_message(request, messages.WARNING, "Enter a stock")
    else:
        try:
            stock = int(stock)
            if stock > 1000:
                messages.add_message(request, messages.WARNING,
                "Enter a lower stock amount")
            elif stock < 0:
                messages.add_message(request, messages.WARNING,
                "Enter a value greater than or equal to 0")
        except ValueError:
            messages.add_message(request, messages.WARNING, "Enter a number")

    return stock

def validate_prescription_items(request, prescription):
    """
    Validates the list of items on a prescription.
    Does not validate item name, as by virtue of having a quantity defined,
    that item will also have a drug as they are created together.
    Accepted parameters are:
    -Must have at least one item
    Accepted parameters for each item are:
    -Must have a stock level (even if it is 0)
    -Must have a non-zero computed perDay value
    """

    if len(prescription.quantity_set.all()) == 0:
        messages.add_message(request, messages.WARNING,
        "Each prescription must have at least one item",
        "#addItem")
    else:
        for quantity in prescription.quantity_set.all():
            if quantity.inStock == -1 or quantity.perDay == 0:
                messages.add_message(request, messages.WARNING,
                "There is information missing from one of your items",
                "#editLink" + str(quantity.id))

def validate_sync_request(request, sync_id):
    """
    Validates a synchronisation request prior to calculation.
    Accepted parameters are:
    -Must have at least two prescriptions
    -Each prescription must be valid (as per above)
    """

    sync_request = SyncRequest.objects.get(id=sync_id)
    if len(sync_request.prescription_set.all()) < 2:
        messages.add_message(request, messages.WARNING,
        "Add at least two prescriptions to synchronise")
    for prescription in sync_request.prescription_set.all():
        validate_prescription_items(request, prescription)

    return sync_request
