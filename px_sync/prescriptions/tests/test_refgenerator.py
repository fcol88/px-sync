from django.test import TestCase
from unittest import mock
from ..models import SyncRequest
from ..reference_service import get_reference, reference_exists
from datetime import datetime

class ReferenceGeneratorTests(TestCase):

    now = datetime(2021, 7, 31)

    def setUp(self):
        syncRequest = SyncRequest()
        syncRequest.reference = get_reference(self.now)
        syncRequest.save()

    def test_generator_creates_date_based_reference(self):
        
        result = get_reference(self.now)

        self.assertEquals('AG', result[:2])
        self.assertEquals(6, len(result))

    def test_when_reference_exists_then_check_returns_true(self):

        syncRequest = SyncRequest()
        reference = get_reference(self.now)
        syncRequest.reference = reference
        syncRequest.save()

        self.assertTrue(reference_exists(reference))
