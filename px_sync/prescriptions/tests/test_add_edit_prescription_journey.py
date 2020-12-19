"""
journey tests for adding/editing prescriptions
as per documentation, if the journey tests are too time
consuming, run python manage.py test --exclude-tag=journey
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.test import TestCase, tag

class AddEditPrescriptionJourney(TestCase):
    """Add/edit prescription test class"""

    def setUp(self):
        """setup method"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/prescriptions/reference")
        continue_link = self.driver.find_element_by_id("continue")
        continue_link.click()

    def tearDown(self):
        """teardown method"""
        self.driver.quit()

    @tag('journey','addpx')
    def test_add_prescription_page_title_is_correct(self):
        """when clicking add prescription, the frequency form is shown
        and the page title is correct"""
        add_prescription = self.driver.find_element_by_id("addPrescription")
        add_prescription.click()
        self.assertIn("How often do you receive your prescription?",
        self.driver.title)

    @tag('journey','addpx')
    def test_add_prescription_page_shows_error_for_invalid_input(self):
        """when submitting an invalid frequency, the user is shown a message
        to help them fix the problem"""
        add_prescription = self.driver.find_element_by_id("addPrescription")
        add_prescription.click()
        frequency = self.driver.find_element_by_id("frequency")
        frequency.send_keys("0")
        save = self.driver.find_element_by_id("save")
        save.click()
        error_pane_exists = True
        try:
            self.driver.find_element_by_id("errorPane")
        except NoSuchElementException:
            error_pane_exists = False
        self.assertIn("How often do you receive your prescription?",
        self.driver.title)
        self.assertTrue(error_pane_exists)

    @tag('journey','addpx')
    def test_add_prescription_page_saves_valid_input_and_redirects(self):
        """when submitting an valid frequency, the user is taken to the
        prescription view page"""
        add_prescription = self.driver.find_element_by_id("addPrescription")
        add_prescription.click()
        frequency = self.driver.find_element_by_id("frequency")
        frequency.send_keys("28")
        save = self.driver.find_element_by_id("save")
        save.click()

        self.assertIn("Add the items on your prescription",
        self.driver.title)

    @tag('journey','addpx')
    def test_edit_frequency_saves_value(self):
        """when submitting an valid frequency, the user is taken to the
        prescription view page"""
        add_prescription = self.driver.find_element_by_id("addPrescription")
        add_prescription.click()
        frequency = self.driver.find_element_by_id("frequency")
        frequency.send_keys("28")
        save = self.driver.find_element_by_id("save")
        save.click()
        self.driver.get("http://localhost:8000/prescriptions/prescriptions")
        saved_frequency = self.driver.find_element_by_id("frequency1").text

        self.assertIn("28", saved_frequency)

        add_prescription = self.driver.find_element_by_id("changeReference1")
        add_prescription.click()
        frequency = self.driver.find_element_by_id("frequency")
        frequency.clear()
        frequency.send_keys("56")
        save = self.driver.find_element_by_id("save")
        save.click()
        self.driver.get("http://localhost:8000/prescriptions/prescriptions")
        saved_frequency = self.driver.find_element_by_id("frequency1").text

        self.assertIn("56", saved_frequency)
