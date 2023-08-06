import selenium
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverRunner:

    def __init__(self):
        self.current_path = os.getcwd()
        self.chromedriver_path = self.current_path + "/chromedriver"
        self.geckodriver_path = self.current_path + "/geckodriver"
        self.driver = webdriver.Chrome(self.chromedriver_path)
        print("Driver loaded...")

    # Go to URL
    def go(self, url):
        self.driver.get(url)

    # Go back one URL
    def back(self):
        self.driver.back()

    # Go forward one URL
    def forward(self):
        self.driver.forward()

    # Search for elements based on XPATH
    def search_elements(self, element, attribute, value):
        wait = WebDriverWait(self.driver, 10)
        try:
            element = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, f"//{element}[@{attribute}='{value}']")))
            if (len(element) > 1):
                return element
            else:
                return element[0]
        except NoSuchElementException:
            return False

    def search_text(self,element,text):
        try:
            wait = WebDriverWait(self.driver, 10)
            elem = wait.until(EC.presence_of_all_elements_located(By.XPATH, f"*//{element}[text()='{text}')]"))
            if (len(elem) > 1):
                return elem
            else:
                return elem[0]
        except NoSuchElementException:
            return False
        
    
    def pause(self, time):
        self.driver.implicitly_wait(time)

    # Click element
    def click_element(self, elem_collec, index=0):
        if(type(elem_collec) == list):
            elem_collec[index].click()
        else:
            elem_collec.click()

    # Close down runner
    def closeDown(self):
        self.driver.close()
        print("Driver closed")
