"""
Validator tests
"""

from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.urls import reverse
from ..models import SyncRequest, Prescription, Quantity, Drug

class ValidatorTests(TestCase):
    """
    Validator test class
    """

    def setUp(self):
        """setup method"""
        sync_request = SyncRequest()
        sync_request.reference = "AA0001"
        sync_request.save()
        prescription_one = Prescription()
        prescription_one.syncRequest = sync_request
        prescription_one.frequency = 1
        prescription_one.save()
        prescription_two = Prescription()
        prescription_two.syncRequest = sync_request
        prescription_two.frequency = 1
        prescription_two.save()
        drug_one = Drug()
        drug_one.name = "Test Drug"
        drug_one.save()
        drug_two = Drug()
        drug_two.name = "Test Drug Too"
        drug_two.save()
        quantity_one = Quantity()
        quantity_one.prescription = prescription_one
        quantity_one.drug = drug_one
        quantity_one.inStock = 1
        quantity_one.perDay = 1
        quantity_one.save()
        quantity_two = Quantity()
        quantity_two.prescription = prescription_two
        quantity_two.drug = drug_two
        quantity_two.inStock = 1
        quantity_two.perDay = 1
        quantity_two.save()
        self.client = Client()
        session = self.client.session
        session['syncid'] = sync_request.id
        session.save()

    def test_when_given_valid_frequency_result_accepted(self):
        """when given a valid frequency, request messages is not populated"""
        response = self.client.post(reverse('frequency'),
        {'frequency' : '28'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 0)

    def test_when_given_blank_frequency_result_rejected(self):
        """when given an empty string, request messages is populated"""
        response = self.client.post(reverse('frequency'),
        {'frequency' : ''})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a frequency')

    def test_when_given_non_numeric_frequency_result_rejected(self):
        """when given a non-integer, request messages is populated"""
        response = self.client.post(reverse('frequency'),
        {'frequency' : 'seven'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a number')

    def test_when_given_too_high_frequency_result_rejected(self):
        """when given a number higher than the threshold,
        request messages is populated"""
        response = self.client.post(reverse('frequency'),
        {'frequency' : '91'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
        "The validator can't be used for prescriptions longer than 90 days")

    def test_when_given_too_low_frequency_result_rejected(self):
        """when given a number less than 1,
        request messages is populated"""
        response = self.client.post(reverse('frequency'),
        {'frequency' : '0'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a number greater than 0')

    def test_when_given_valid_name_result_accepted(self):
        """when given a valid drug name, request messages is not populated"""
        response = self.client.post(reverse('itemname', args=[1]),
        {'drugname' : 'A Drug'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 0)

    def test_when_given_blank_name_result_rejected(self):
        """when given an empty drug name, request messages is populated"""
        response = self.client.post(reverse('itemname', args=[1]),
        {'drugname' : ''})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a drug name')

    def test_when_given_valid_period_and_dosage_result_accepted(self):
        """when given a valid period and dosage, messages is not populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : '1', 'dosage-days' : '1'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 0)

    def test_when_given_no_period_result_rejected(self):
        """when given no period, messages is populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : ''})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Choose a period')

    def test_when_given_invalid_period_result_rejected(self):
        """when given an invalid period, messages is populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : '0'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Choose a valid period')

    def test_when_given_valid_period_and_no_dosage_result_rejected(self):
        """when given a valid period and no dosage, messages is populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : '1', 'dosage-days' : ''})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a dosage')

    def test_when_given_too_high_daily_dose_result_rejected(self):
        """when given an valid period and a dosage beyond the maximum,
        messages is populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : '1', 'dosage-days' : '21'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a lower dosage')

    def test_when_given_too_high_weekly_dose_result_rejected(self):
        """when given an valid period and a dosage beyond the maximum,
        messages is populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : '7', 'dosage-weeks' : '141'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a lower dosage')

    def test_when_given_too_low_dose_result_rejected(self):
        """when given an valid period and a dosage beyond the maximum,
        messages is populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : '7', 'dosage-weeks' : '141'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a lower dosage')

    def test_when_given_non_numeric_dose_result_rejected(self):
        """when given an valid period and a dosage beyond the maximum,
        messages is populated"""
        response = self.client.post(reverse('dosage', args=[1]),
        {'period' : '7', 'dosage-weeks' : 'four'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a number')

    def test_when_given_valid_stock_result_accepted(self):
        """when given a valid stock, messages is not populated"""
        response = self.client.post(reverse('stock', args=[1]),
        {'stock' : '2'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 0)

    def test_when_given_too_high_stock_result_rejected(self):
        """when given a stock over the threshold,
        messages is populated"""
        response = self.client.post(reverse('stock', args=[1]),
        {'stock' : '1001'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a lower stock amount')

    def test_when_given_too_low_stock_result_rejected(self):
        """when given a stock under the threshold,
        messages is populated"""
        response = self.client.post(reverse('stock', args=[1]),
        {'stock' : '-1'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a value greater than or equal to 0')

    def test_when_given_non_numeric_stock_result_rejected(self):
        """when given a stock under the threshold,
        messages is populated"""
        response = self.client.post(reverse('stock', args=[1]),
        {'stock' : 'two'})
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Enter a number')

    def test_when_given_a_valid_prescription_result_accepted(self):
        """when given a prescription with only valid items,
        messages is not populated"""
        response = self.client.get(reverse('checkitems', args=[1]))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 0)

    def test_when_prescription_has_an_invalid_stock_result_rejected(self):
        """when given a prescription where the stock is still the default,
        messages is populated"""
        quantity = Quantity.objects.get(id=1)
        quantity.inStock = -1
        quantity.save()
        response = self.client.get(reverse('checkitems', args=[1]))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
        'There is information missing from one of your items')

    def test_when_prescription_has_an_invalid_per_day_result_rejected(self):
        """when given a prescription where the computed per day amount
        is still the default, messages is populated"""
        quantity = Quantity.objects.get(id=1)
        quantity.perDay = 0
        quantity.save()
        response = self.client.get(reverse('checkitems', args=[1]))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
        'There is information missing from one of your items')

    def test_when_sync_request_has_two_or_more_items_result_accepted(self):
        """when given a sync request where there are two prescriptions
        which both have only valid items, messages is not populated"""
        response = self.client.get(reverse('calculate'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 0)

    def test_when_sync_request_has_less_than_two_items_result_rejected(self):
        """when given a sync request where there are two prescriptions
        which both have only valid items, messages is not populated"""
        prescription = Prescription.objects.get(id=2)
        prescription.delete()
        response = self.client.get(reverse('calculate'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
        'Add at least two prescriptions to synchronise')
