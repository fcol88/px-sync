from django.test import TestCase
from ..models import SyncRequest, Prescription, Quantity, Drug

class ModelTests(TestCase):
    def setUp(self):
        pass

    def test_syncrequest_instantiates(self):

        syncRequest = SyncRequest()
        self.assertIsInstance(syncRequest, SyncRequest)

    def test_syncrequest_sets_created_date(self):

        syncRequest = SyncRequest()
        syncRequest.reference = 'TEST01'

        self.assertIsNone(syncRequest.created)

        syncRequest.save()

        self.assertIsNotNone(syncRequest.created)

    def test_prescription_instantiates(self):

        prescription = Prescription()
        self.assertIsInstance(prescription, Prescription)
        
    def test_quantity_instantiates(self):

        quantity = Quantity()
        self.assertIsInstance(quantity, Quantity)

    def test_drug_instantiates(self):

        drug = Drug()
        self.assertIsInstance(drug, Drug)