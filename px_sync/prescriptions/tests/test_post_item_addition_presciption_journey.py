"""
journey tests for viewing prescriptions after addition
and viewing sync request
as per documentation, if the journey tests are too time
consuming, run python manage.py test--exclude-tag=journey
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.test import TestCase, tag

class PostItemAdditionPrescriptionJourney(TestCase):
    """Post-item addition prescription test class"""

    def setUp(self):
        """setup method"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/prescriptions/reference")
        cont = self.driver.find_element_by_id("continue")
        cont.click()

    def tearDown(self):
        """teardown method"""
        self.driver.quit()

    def make_valid_prescription(self):
        """make valid item and save"""
        self.driver.get("http://localhost:8000/prescriptions/frequency")
        frequency = self.driver.find_element_by_id("frequency")
        frequency.send_keys("28")
        save = self.driver.find_element_by_id("save")
        save.click()
        add_item = self.driver.find_element_by_id("addItem")
        add_item.click()
        drug_name = self.driver.find_element_by_id("drugname")
        drug_name.send_keys("Test Item")
        next_link = self.driver.find_element_by_id("next")
        next_link.click()
        period_days = self.driver.find_element_by_id("period-days")
        period_days.click()
        dosage_days = self.driver.find_element_by_id("dosage-days")
        dosage_days.send_keys("4")
        next_link = self.driver.find_element_by_id("next")
        next_link.click()
        stock = self.driver.find_element_by_id("stock")
        stock.send_keys("4")
        save_link = self.driver.find_element_by_id("save")
        save_link.click()

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
        continue_link_exists = True
        try:
            self.driver.find_element_by_id("submit")
        except NoSuchElementException:
            continue_link_exists = False

        self.assertFalse(continue_link_exists)

    @tag('journey','postpx')
    def test_view_prescriptions_shows_submit_link_when_valid(self):
        """when two or more prescriptions have been added, the user has a
        link to click"""

        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        PostItemAdditionPrescriptionJourney.make_valid_prescription(self)
        self.driver.get("http://localhost:8000/prescriptions/prescriptions")
        continue_link_exists = True
        try:
            self.driver.find_element_by_id("submit")
        except NoSuchElementException:
            continue_link_exists = False

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
