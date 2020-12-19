"""
journey tests for creation journey.
as per documentation, if the journey tests are too time
consuming, run python manage.py test --exclude-tag=journey
"""

from selenium import webdriver
from django.test import TestCase, tag
from .journey_test_utils import check_element_exists

class CreateJourneyTests(TestCase):
    """Create journey test class"""

    def setUp(self):
        """setup method"""
        self.driver = webdriver.Chrome()

    def tearDown(self):
        """teardown method"""
        self.driver.quit()

    @tag('journey','create')
    def test_landing_page_title_is_correct(self):
        """when visiting the landing page, the title
        is rendered correctly"""
        self.driver.get("http://localhost:8000/prescriptions/start")

        self.assertIn("Synchronise your prescriptions", self.driver.title)

    @tag('journey','create')
    def test_landing_page_returns_not_found_when_not_found(self):
        """when the user enters an invalid reference, they are shown
        a message telling them the reference couldn't be found"""
        self.driver.get("http://localhost:8000/prescriptions/start")
        reference = self.driver.find_element_by_id("reference")
        reference.send_keys("REFREF")
        continue_link = self.driver.find_element_by_id("continueLink")
        continue_link.click()
        error_pane_exists = check_element_exists(self.driver, "errorPane")

        self.assertIn("Synchronise your prescriptions", self.driver.title)
        self.assertTrue(error_pane_exists)


    @tag('journey','create')
    def test_landing_page_redirects_to_reference_page(self):
        """when clicking the start button, a reference is generated
        and the user is redirected to the reference page"""
        self.driver.get("http://localhost:8000/prescriptions/start")
        reference = self.driver.find_element_by_id("startLink")
        reference.click()

        self.assertIn("Your unique reference", self.driver.title)

    @tag('journey','create')
    def test_reference_page_redirects_to_prescriptions_view(self):
        """when clicking through from the reference page, the user
        is taken to the screen for entering prescriptions"""
        self.driver.get("http://localhost:8000/prescriptions/reference")
        cont = self.driver.find_element_by_id("continue")
        cont.click()

        self.assertIn("Add your prescriptions", self.driver.title)

    @tag('journey','create')
    def test_landing_page_redirects_to_prescriptions_view_when_found(self):
        """when a valid reference is entered into the continue form,
        the user is redirected to the screen for entering prescriptions"""
        self.driver.get("http://localhost:8000/prescriptions/reference")
        reference = self.driver.find_element_by_id("reference").text
        self.driver.get("http://localhost:8000/prescriptions/start")
        reference_input = self.driver.find_element_by_id("reference")
        reference_input.send_keys(reference)
        continue_link = self.driver.find_element_by_id("continueLink")
        continue_link.click()

        self.assertIn("Add your prescriptions", self.driver.title)
