"""
journey tests for searching and viewing requests
as per documentation, if the journey tests are too time
consuming, run python manage.py test --exclude-tag=journey
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from prescriptions.models import SyncRequest, Prescription, Quantity, Drug
from .login_test_util import login

class SearchViewJourney(StaticLiveServerTestCase):
    """Search/view journey test class"""

    def setUp(self):
        """setup method"""
        super().setUp()
        self.driver = webdriver.Chrome()
        #create user
        self.user = get_user_model().objects.create_superuser(username="test",
        password="password",
        email="test@test.com")
        self.user.save()
        #create sync request
        sync_request = SyncRequest()
        sync_request.reference = "TEST01"
        sync_request.save()
        #create two prescriptions
        prescription_one = Prescription()
        prescription_one.frequency = 28
        prescription_one.syncRequest = sync_request
        prescription_one.save()
        prescription_two = Prescription()
        prescription_two.frequency = 28
        prescription_two.syncRequest = sync_request
        prescription_two.save()
        #create two drugs
        drug_one = Drug()
        drug_one.name = "Drug One"
        drug_one.save()
        drug_two = Drug()
        drug_two.name = "Drug Two"
        drug_two.save()
        #create two quantities
        quantity_one = Quantity()
        quantity_one.drug = drug_one
        quantity_one.prescription = prescription_one
        quantity_one.dosage = 1
        quantity_one.period = 1
        quantity_one.perDay = 1
        quantity_one.inStock = 1
        quantity_one.rawStock = 1
        quantity_one.required = 27
        quantity_one.save()
        quantity_two = Quantity()
        quantity_two.drug = drug_two
        quantity_two.prescription = prescription_two
        quantity_two.dosage = 1
        quantity_two.period = 1
        quantity_two.perDay = 1
        quantity_two.inStock = 28
        quantity_two.rawStock = 28
        quantity_two.required = 0
        quantity_two.save()
        #log in to application
        login(self.driver, self.live_server_url)

    def tearDown(self):
        """teardown method"""
        self.driver.quit()
        super().tearDown()

    @tag('journey','view')
    def test_search_returns_not_found_message_when_invalid(self):
        """when the user provides a reference that isn't found, they're shown
        a message to advise them it was incorrect"""
        search = self.driver.find_element_by_id("search")
        search.send_keys("THX1138")
        search_button = self.driver.find_element_by_id("searchButton")
        search_button.click()
        error_pane_exists = False
        try:
            self.driver.find_element_by_id("errorPane")
        except NoSuchElementException:
            error_pane_exists = True

        self.assertIn("Search for a prescription synchronisation request",
        self.driver.title)
        self.assertTrue(error_pane_exists)

    @tag('journey','view')
    def test_search_redirects_to_view_when_sync_found(self):
        """when the user provides a reference that is found, they're redirected
        to the view page"""
        search = self.driver.find_element_by_id("search")
        search.send_keys("TEST01")
        search_button = self.driver.find_element_by_id("searchButton")
        search_button.click()

        self.assertIn("Prescription synchronisation request",
        self.driver.title)
        self.assertIn("view", self.driver.current_url)
