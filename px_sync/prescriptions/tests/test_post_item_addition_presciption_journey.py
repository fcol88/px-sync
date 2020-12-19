"""
journey tests for viewing prescriptions after addition
and viewing sync request
as per documentation, if the journey tests are too time
consuming, run python manage.py test--exclude-tag=journey
"""

from selenium import webdriver
from django.test import TestCase, tag
from .journey_test_utils import add_valid_drug_name, add_valid_period,\
add_valid_stock, create_sync_request, add_valid_frequency, check_element_exists

class PostItemAdditionPrescriptionJourney(TestCase):
    """Post-item addition prescription test class"""

    def setUp(self):
        """setup method"""
        self.driver = webdriver.Chrome()
        create_sync_request(self.driver)

    def tearDown(self):
        """teardown method"""
        self.driver.quit()

    def make_valid_prescription(self):
        """make valid item and save"""
        add_valid_frequency(self.driver)
        add_valid_drug_name(self.driver)
        add_valid_period(self.driver)
        add_valid_stock(self.driver)

    @tag('journey','postpx')
    def test_view_prescription_link_shows_prescription_details(self):
        """when clicking the view link after adding a prescription,
        the view link takes the user to that prescription to view"""

        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        self.driver.get("http://localhost:8000/prescriptions/prescriptions")
        item_name = self.driver.find_element_by_id("item1-1").text

        self.assertIn("Test Item", item_name)

        view_link = self.driver.find_element_by_id("viewLink1")
        view_link.click()
        item_name = self.driver.find_element_by_id("drugname1").text

        self.assertIn("Add the items on your prescription", self.driver.title)
        self.assertIn("Test Item", item_name)

    @tag('journey','postpx')
    def test_view_prescriptions_has_no_submit_link_when_invalid(self):
        """when there are less than two prescriptions, the submit button is
        not shown"""

        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        self.driver.get("http://localhost:8000/prescriptions/prescriptions")
        continue_link_exists = check_element_exists(self.driver, "submit")

        self.assertFalse(continue_link_exists)

    @tag('journey','postpx')
    def test_view_prescriptions_shows_submit_link_when_valid(self):
        """when two or more prescriptions have been added, the user has a
        link to click"""

        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        self.driver.get("http://localhost:8000/prescriptions/prescriptions")
        continue_link_exists = check_element_exists(self.driver, "submit")

        self.assertTrue(continue_link_exists)

    @tag('journey','postpx')
    def test_view_prescriptions_redirects_to_sync_view_when_valid(self):
        """when two or more prescriptions have been added, the user has a
        link to click"""

        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        self.driver.get("http://localhost:8000/prescriptions/prescriptions")
        continue_link = self.driver.find_element_by_id("submit")
        continue_link.click()

        self.assertIn("Your prescription synchronisation request",
        self.driver.title)
