"""
journey tests for logging in/checking users are authenticated
as per documentation, if the journey tests are too time
consuming, run python manage.py test --exclude-tag=journey
"""

from selenium import webdriver
from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from .login_test_util import login

class LoginJourney(StaticLiveServerTestCase):
    """Login journey test class"""

    def setUp(self):
        """setup method"""
        super().setUp()
        self.driver = webdriver.Chrome()
        self.user = get_user_model().objects.create_superuser(username="test",
        password="password",
        email="test@test.com")
        self.user.save()

    def tearDown(self):
        """teardown method"""
        self.driver.quit()
        super().tearDown()

    @tag('journey','login')
    def test_login_page_renders(self):
        """when the user visits the login page, the page renders correctly"""
        self.driver.get(self.live_server_url+"/prescriber/login")
        self.assertIn("Prescription Synchronisation Requests", self.driver.title)

    @tag('journey','login')
    def test_search_redirects_to_login(self):
        """when the user visits the login page and logs in, they are redirected
        to the search page"""
        self.driver.get(self.live_server_url+"/prescriber/search")

        self.assertIn("Prescription Synchronisation Requests",
        self.driver.title)

    @tag('journey','login')
    def test_view_redirects_to_login(self):
        """when the user visits the view page when unauthenticated,
        they are redirected to the login page"""
        self.driver.get(self.live_server_url+"/prescriber/view/1")

        self.assertIn("Prescription Synchronisation Requests",
        self.driver.title)

    @tag('journey','login')
    def test_login_page_redirects_to_search(self):
        """when the user logs in, they are redirected to the search page"""
        login(self.driver, self.live_server_url)
        self.assertIn("Search for a prescription synchronisation request", self.driver.title)
    