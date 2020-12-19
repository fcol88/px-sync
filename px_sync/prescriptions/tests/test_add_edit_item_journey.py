"""
journey tests for adding/editing items
as per documentation, if the journey tests are too time
consuming, run python manage.py test--exclude-tag=journey
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from django.test import TestCase, tag

class AddEditItemJourney(TestCase):
    """Add/edit item test class"""

    def setUp(self):
        """setup method"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/prescriptions/reference")
        cont = self.driver.find_element_by_id("continue")
        cont.click()
        self.driver.get("http://localhost:8000/prescriptions/frequency")
        frequency = self.driver.find_element_by_id("frequency")
        frequency.send_keys("28")
        save = self.driver.find_element_by_id("save")
        save.click()

    def tearDown(self):
        """teardown method"""
        self.driver.quit()

    def make_valid_item(self):
        """creates valid item and saves"""
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

    @tag('journey','additem')
    def test_add_item_page_title_is_correct(self):
        """when clicking add item, the drug name form is shown
        and the page title is correct"""
        add_item = self.driver.find_element_by_id("addItem")
        add_item.click()

        self.assertIn("Tell us about the item on your prescription",
        self.driver.title)
        self.assertIn("itemname", self.driver.current_url)

    @tag('journey','additem')
    def test_add_item_page_shows_error_for_invalid_item_name(self):
        """when submitting an invalid drug name, the user is shown a message
        to help them fix the problem"""
        add_item = self.driver.find_element_by_id("addItem")
        add_item.click()
        next_link = self.driver.find_element_by_id("next")
        next_link.click()
        error_pane_exists = True
        try:
            self.driver.find_element_by_id("errorPane")
        except NoSuchElementException:
            error_pane_exists = False

        self.assertIn("itemname", self.driver.current_url)
        self.assertTrue(error_pane_exists)

    @tag('journey','additem')
    def test_add_item_page_redirects_when_input_is_valid(self):
        """when submitting a valid drug name, the user is redirected to
        the dosage page"""
        add_item = self.driver.find_element_by_id("addItem")
        add_item.click()
        drug_name = self.driver.find_element_by_id("drugname")
        drug_name.send_keys("Test Item")
        next_link = self.driver.find_element_by_id("next")
        next_link.click()

        self.assertIn("Tell us about the item on your prescription",
        self.driver.title)
        self.assertIn("dosage", self.driver.current_url)

    @tag('journey','additem')
    def test_dosage_page_shows_error_for_invalid_dosage(self):
        """when submitting an invalid dosage and period, the user is shown a
        message to help them fix the problem"""
        add_item = self.driver.find_element_by_id("addItem")
        add_item.click()
        drug_name = self.driver.find_element_by_id("drugname")
        drug_name.send_keys("Test Item")
        next_link = self.driver.find_element_by_id("next")
        next_link.click()
        next_link = self.driver.find_element_by_id("next")
        next_link.click()
        error_pane_exists = True
        try:
            self.driver.find_element_by_id("errorPane")
        except NoSuchElementException:
            error_pane_exists = False

        self.assertIn("dosage", self.driver.current_url)
        self.assertTrue(error_pane_exists)

    @tag('journey','additem')
    def test_dosage_page_redirects_when_valid_dosage(self):
        """when submitting a valid dosage and period, the user is redirected
        to the stock page"""
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

        self.assertIn("Tell us about the item on your prescription",
        self.driver.title)
        self.assertIn("stock", self.driver.current_url)

    @tag('journey','additem')
    def test_stock_page_shows_error_when_invalid_stock(self):
        """when submitting an invalid stock, the user is shown a message
        to help them correct the error"""
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
        save_link = self.driver.find_element_by_id("save")
        save_link.click()
        error_pane_exists = True
        try:
            self.driver.find_element_by_id("errorPane")
        except NoSuchElementException:
            error_pane_exists = False

        self.assertIn("stock", self.driver.current_url)
        self.assertTrue(error_pane_exists)

    @tag('journey','additem')
    def test_stock_page_redirects_when_valid_stock(self):
        """when submitting a valid stock, the user is redirected
        to the prescription view page, and the continue link is
        shown"""
        AddEditItemJourney.make_valid_item(self)
        check_items_link_exists = True
        try:
            self.driver.find_element_by_id("checkitems")
        except NoSuchElementException:
            check_items_link_exists = False

        self.assertIn("Add the items on your prescription",
        self.driver.title)
        self.assertTrue(check_items_link_exists)

    @tag('journey','additem')
    def test_check_items_redirects_to_prescriptions_view_when_valid(self):
        """when clicking on the continue button with a valid item,
        the user is redirected to the prescriptions page"""
        AddEditItemJourney.make_valid_item(self)
        check_items = self.driver.find_element_by_id("checkitems")
        check_items.click()

        self.assertIn("Add your prescriptions", self.driver.title)

    @tag('journey','additem')
    def test_edit_item_saves_new_values(self):
        """when editing an item, the updated values are saved"""
        AddEditItemJourney.make_valid_item(self)

        drug_name = self.driver.find_element_by_id("drugname1").text
        dosage = self.driver.find_element_by_id("dosage1").text
        in_stock = self.driver.find_element_by_id("instock1").text

        self.assertIn("Test Item", drug_name)
        self.assertIn("4", dosage)
        self.assertIn("day", dosage)
        self.assertIn("4", in_stock)

        edit_link = self.driver.find_element_by_id("editLink1")
        edit_link.click()
        drug_name_input = self.driver.find_element_by_id("drugname")
        drug_name_input.clear()
        drug_name_input.send_keys("New Drug")
        next_link = self.driver.find_element_by_id("next")
        next_link.click()
        period_weeks = self.driver.find_element_by_id("period-weeks")
        period_weeks.click()
        dosage_weeks = self.driver.find_element_by_id("dosage-weeks")
        dosage_weeks.send_keys("1")
        next_link = self.driver.find_element_by_id("next")
        next_link.click()
        stock = self.driver.find_element_by_id("stock")
        stock.clear()
        stock.send_keys("2")
        save_link = self.driver.find_element_by_id("save")
        save_link.click()

        drug_name = self.driver.find_element_by_id("drugname1").text
        dosage = self.driver.find_element_by_id("dosage1").text
        in_stock = self.driver.find_element_by_id("instock1").text

        self.assertIn("New Drug", drug_name)
        self.assertIn("1", dosage)
        self.assertIn("week", dosage)
        self.assertIn("2", in_stock)
