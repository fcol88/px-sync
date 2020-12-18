"""
Calculator for stock values and final synchronisation calculation
"""

from math import ceil

def calculate_stock_value(quantity, stock):
    """
    Calculates the stock value to store on a prescription.
    If their stock is beyond what they'd take on a daily basis,
    it caps it to the nearest tablet/caplet/etc.
    Otherwise it returns the input stock amount.
    """

    maximum = quantity.prescription.frequency * quantity.perDay
    rounded_maximum = ceil(maximum)

    if stock > rounded_maximum:
        return rounded_maximum, stock
    return stock, stock

def calculate_required_items(sync_request):
    """
    Loops through each prescription item and saves the required amount.
    If the user has previously ran this calculation, and the
    details of the prescription have changed such that a new
    drug contains the maximum, it zeroes whatever quantity was
    previously calculated for the new drug.
    """

    maximum, max_id = get_maximum(sync_request)

    for prescription in sync_request.prescription_set.all():

        for quantity in prescription.quantity_set.all():

            if quantity.id != max_id:
                quantity.required = get_required_stock(quantity, maximum)
            else:
                quantity.required = 0
            quantity.save()

def get_maximum(sync_request):
    """
    Gets the maximum number of days in stock, and the ID
    of the item with the maximum stock
    """

    maximum = 0
    max_id = None

    for prescription in sync_request.prescription_set.all():

        for quantity in prescription.quantity_set.all():

            stock_in_days = quantity.inStock / quantity.perDay

            if stock_in_days > maximum:
                max_id = quantity.id
                maximum = stock_in_days

    return maximum, max_id

def get_required_stock(quantity, maximum):
    """
    Calculates the required stock for an item, rounding
    up to the nearest whole tablet/caplet/etc.
    """

    stock_in_days = quantity.inStock / quantity.perDay
    required_amount = (maximum - stock_in_days) * quantity.perDay
    rounded_required_amount = ceil(required_amount)
    return rounded_required_amount
