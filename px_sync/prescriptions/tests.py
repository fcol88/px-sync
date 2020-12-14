from django.test import TestCase
from prescriptions.models import SyncRequest, Prescription, Quantity, Drug

class PrescriptionTests(TestCase):
    def setUp(self):
        pass

    def test_syncrequest_instantiates(self):

        syncRequest = SyncRequest()
        self.assertIsInstance(syncRequest, SyncRequest)

    def test_prescription_instantiates(self):

        prescription = Prescription()
        self.assertIsInstance(prescription, Prescription)
        
    def test_quantity_instantiates(self):

        quantity = Quantity()
        self.assertIsInstance(quantity, Quantity)

    def test_drug_instantiates(self):

        drug = Drug()
        self.assertIsInstance(drug, Drug)