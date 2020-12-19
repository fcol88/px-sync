"""
common code for logging in placed in separate file
"""

def login(driver, live_server_url):
    """
    logs in to application given a selenium driver and the server url
    """
    driver.get(live_server_url+"/prescriber/login")
    username = driver.find_element_by_id("username")
    username.send_keys("test")
    password = driver.find_element_by_id("password")
    password.send_keys("password")
    login_button = driver.find_element_by_id("login")
    login_button.click()
