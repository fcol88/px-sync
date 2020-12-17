"""
Reference service tests
"""

from datetime import datetime
from django.test import TestCase
from ..models import SyncRequest
from ..reference_service import get_reference, reference_exists

class ReferenceGeneratorTests(TestCase):
    """
    Reference service test class
    """

    ag = datetime(2021, 7, 31)
    ba = datetime(2023, 3, 1)

    def setUp(self):
        """setup method"""
        sync_request = SyncRequest()
        sync_request.reference = get_reference(self.ag)
        sync_request.save()

    def test_generator_creates_date_based_reference(self):
        """When a date is passed in, a 6-character string is returned
        where the first two are based on the date provided"""
        result = get_reference(self.ag)

        self.assertEqual('AG', result[:2])
        self.assertEqual(6, len(result))

        result = get_reference(self.ba)

        self.assertEqual('BA', result[:2])
        self.assertEqual(6, len(result))

    def test_when_reference_exists_then_check_returns_true(self):
        """When a reference exists in the database, this is flagged"""

        sync_request = SyncRequest()
        reference = get_reference(self.ag)
        sync_request.reference = reference
        sync_request.save()

        self.assertTrue(reference_exists(reference))
