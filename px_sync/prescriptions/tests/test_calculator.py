"""
Calculator tests
"""

from django.test import TestCase
from prescriptions import calculator
from ..models import Quantity, SyncRequest, Prescription, Drug

class CalculatorTests(TestCase):
    """
    Calculator test class
    """

    def setUp(self):
        "setup method which creates objects to calculate with"
        sync_request = SyncRequest()
        sync_request.reference = "AA0001"
        sync_request.save()
        prescription_one = Prescription()
        prescription_one.frequency = 28
        prescription_one.syncRequest = sync_request
        prescription_one.save()
        prescription_two = Prescription()
        prescription_two.frequency = 11
        prescription_two.syncRequest = sync_request
        prescription_two.save()
        drug_one = Drug()
        drug_one.save()
        drug_two = Drug()
        drug_two.save()
        quantity_one = Quantity()
        quantity_one.perDay = 0.5
        quantity_one.inStock = 12
        quantity_one.drug = drug_one
        quantity_one.prescription = prescription_one
        quantity_one.save()
        quantity_two = Quantity()
        quantity_two.perDay = 0.1
        quantity_two.inStock = 3
        quantity_two.drug = drug_two
        quantity_two.prescription = prescription_two
        quantity_two.save()

    def test_calculator_returns_stock_when_below_maximum(self):
        """When the stock is below maximum, return the stock value"""
        quantity = Quantity.objects.get(id=1)
        result = calculator.calculate_stock_value(quantity, quantity.inStock)

        self.assertEqual(result, 12)

    def test_calculator_returns_maximum_when_above_maximum(self):
        """When the stock is above maximum, return the maximum"""
        quantity = Quantity.objects.get(id=2)
        result = calculator.calculate_stock_value(quantity, quantity.inStock)

        self.assertEqual(result, 2)

    def test_calculator_calculates_required_quantities(self):
        """when given a list of prescriptions, 
        the required amount will be calculated and saved"""
        sync_request = SyncRequest.objects.get(id=1)
        calculator.calculate_required_items(sync_request)

        quantity_one = Quantity.objects.get(id=1)
        quantity_two = Quantity.objects.get(id=2)

        self.assertEqual(quantity_one.required, 3)
        self.assertEqual(quantity_two.required, 0)

    def test_calculator_zeros_required_amount_when_max_drug_changes(self):
        """when given a list of prescriptions, 
        the required amount will be calculated and saved"""

        sync_request = SyncRequest.objects.get(id=1)
        calculator.calculate_required_items(sync_request)

        quantity = Quantity.objects.get(id=1)
        quantity.inStock = 30
        quantity.save()

        sync_request = SyncRequest.objects.get(id=1)
        calculator.calculate_required_items(sync_request)

        quantity_one = Quantity.objects.get(id=1)
        quantity_two = Quantity.objects.get(id=2)

        self.assertEqual(quantity_one.required, 0)
        self.assertEqual(quantity_two.required, 3)

    def test_get_maximum_gets_maximum_and_id(self):
        """
        When given a list of prescriptions,
        the maximum number of days and corresponding
        id will be returned
        """
        sync_request = SyncRequest.objects.get(id=1)
        maximum, max_id = calculator.get_maximum(sync_request)

        self.assertEqual(maximum, 30)
        self.assertEqual(max_id, 2)

    def test_get_required_stock_gets_required_stock(self):
        """
        When given a quantity, the amount required to
        bring the item in line with the maximum is returned
        """
        quantity = Quantity.objects.get(id=1)
        result = calculator.get_required_stock(quantity, 26)

        self.assertEqual(result, 1)

    def test_get_required_stock_rounds_up(self):
        """
        When given a quantity which would otherwise be a decimal,
        the return is rounded up to the nearest integer
        """
        quantity = Quantity.objects.get(id=2)
        result = calculator.get_required_stock(quantity, 31)

        self.assertEqual(result, 1)
