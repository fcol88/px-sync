"""
utils used in prescriptions journey tests to avoid code duplication
"""

from selenium.common.exceptions import NoSuchElementException

def create_sync_request(driver):
    """creates sync request and moves to prescription view page"""
    driver.get("http://localhost:8000/prescriptions/reference")
    cont = driver.find_element_by_id("continue")
    cont.click()

def add_valid_frequency(driver):
    """jumps to frequency form, provides valid input and submits"""
    driver.get("http://localhost:8000/prescriptions/frequency")
    frequency = driver.find_element_by_id("frequency")
    frequency.send_keys("28")
    save = driver.find_element_by_id("save")
    save.click()

def add_valid_drug_name(driver):
    """clicks add item, provides valid name and submits"""
    add_item = driver.find_element_by_id("addItem")
    add_item.click()
    drug_name = driver.find_element_by_id("drugname")
    drug_name.send_keys("Test Item")
    next_link = driver.find_element_by_id("next")
    next_link.click()

def add_valid_period(driver):
    """from period page, adds valid period and dosage and submits"""
    period_days = driver.find_element_by_id("period-days")
    period_days.click()
    dosage_days = driver.find_element_by_id("dosage-days")
    dosage_days.send_keys("4")
    next_link = driver.find_element_by_id("next")
    next_link.click()

def add_valid_stock(driver):
    """from stock page, adds valid stock and submits"""
    stock = driver.find_element_by_id("stock")
    stock.send_keys("4")
    save_link = driver.find_element_by_id("save")
    save_link.click()

def check_element_exists(driver, element_id):
    """returns true if element exists, else returns false"""
    try:
        driver.find_element_by_id(element_id)
        return True
    except NoSuchElementException:
        return False
