from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.options import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


firefox_options = Options()
firefox_options.add_argument("--disable-infobars")
firefox_options.add_argument("--disable-extensions")
firefox_options.add_argument("--disable-popup-blocking")

profile_options = FirefoxProfile()
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0'
profile_options.set_preference('profile_options = FirefoxProfile()', user_agent)
profile_options.set_preference("print_printer", "Mozilla Save to PDF")
profile_options.set_preference("print.always_print_silent", True)
profile_options.set_preference("print.show_print_progress", False)
profile_options.set_preference('print.save_as_pdf.links.enabled', True)
profile_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)

driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=firefox_options,
                           firefox_profile=profile_options)



# URL = "https://clutch.co/profile/naked#summary"

# driver.get(URL)

# x=driver.find_element(By.XPATH, "//*[@class='tel']/.//span[contains(@class,'value')]")
# print(x.get_attribute('innerHTML'))

def find_firm_contact(url):
    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=firefox_options,
                           firefox_profile=profile_options)

    driver.get(url)
    x=driver.find_element(By.XPATH, "//*[@class='tel']/.//span[contains(@class,'value')]")
    contact = x.get_attribute('innerHTML')
    driver.close()
    return contact


def get_service_location(url, service):
    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=firefox_options,
                           firefox_profile=profile_options)

    driver.get(url)
    service_input =  driver.find_element_by_id("services")
    #service_input.send_keys(service)
    search_span = f"//span[contains(., '{service}')]"
    driver.find_element_by_css_selector("input[aria-controls='services_dropdown']").click()
    sleep(5)
    driver.find_element(By.XPATH, "//span[contains(text(),'Mobile App Development')]").click();
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='facets_list__item__name']/.//span[contains(.,'Mobile App Development')]"))).click()
    #x=driver.find_element(By.XPATH, "//*[@class='facets_list facets_list__location']/.//span[contains(@class,'name')]");
    sleep(7)
    x=driver.find_elements_by_xpath('//div[contains(@id, "location_list")]//a[contains(@href, "#")]')
    location_list = [i.get_attribute('aria-label') for i in x]
    ids=driver.find_elements_by_xpath('//input[contains(@name, "location")]')
    location_id_list = [id.get_attribute('value') for id in ids]
    location_id_list.pop(0)
    zipped_location = zip(location_list, location_id_list)
    driver.close()
    return zipped_location


if __name__ == "__main__":
    get_service_location("https://clutch.co", "Mobile App Development")
