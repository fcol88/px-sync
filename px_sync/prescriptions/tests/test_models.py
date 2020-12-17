"""
Model tests
"""

from django.test import TestCase
from ..models import SyncRequest, Prescription, Quantity, Drug

class ModelTests(TestCase):
    """
    Model test class
    """

    def test_syncrequest_instantiates(self):
        """new syncrequest is instance of syncrequest"""
        sync_request = SyncRequest()
        self.assertIsInstance(sync_request, SyncRequest)

    def test_syncrequest_sets_created_date(self):
        """when saved, the syncrequest created date is set"""
        sync_request = SyncRequest()
        sync_request.reference = 'TEST01'

        self.assertIsNone(sync_request.created)

        sync_request.save()

        self.assertIsNotNone(sync_request.created)

    def test_prescription_instantiates(self):
        """new prescription is instantiated"""
        prescription = Prescription()
        self.assertIsInstance(prescription, Prescription)
        self.assertEqual(prescription.frequency, 0)

    def test_quantity_instantiates(self):
        """new quantity is instantiated"""
        quantity = Quantity()
        self.assertIsInstance(quantity, Quantity)
        self.assertEqual(quantity.dosage, -1)
        self.assertEqual(quantity.period, -1)
        self.assertEqual(quantity.inStock, -1)
        self.assertEqual(quantity.required, 0)
        self.assertEqual(quantity.perDay, 0)

    def test_drug_instantiates(self):
        """new drug is instantiated"""
        drug = Drug()
        self.assertIsInstance(drug, Drug)
