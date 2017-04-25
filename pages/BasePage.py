#coding=utf-8

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *


class BasePage(object):
    #The basic class for various pages

    def __init__(self,driver):
        try:
            self.driver = driver
            self.driver.delete_all_cookies()
        except Exception:
            raise NoSuchAttributeException("delete_all_cookies() method is not supported.")

    def findElement(self,element):
        try:
            type = element[0].strip().lower()
            value = element[1].strip()

            if type == 'id':
                elem = self.driver.find_element_by_id(value)
            elif type == 'name':
                elem = self.driver.find_element_by_name(value)
            elif type == 'class':
                elem = self.driver.find_element_by_class_name(value)
            elif type == 'css':
                elem = self.driver.find_element_by_css_selector(value)
            elif type == 'tag':
                elem = self.driver.find_element_by_tag_name(value)
            elif type == 'link_text':
                elem = self.driver.find_element_by_link_text(value)
            elif type == 'xpath':
                elem = self.driver.find_element_by_xpath(value)
            else:
                raise NameError("Please correct the type in function parameter.")
        except Exception:
            raise ValueError("No such element found "+str(element))
        return elem

    def findElements(self,element):
        try:
            type = element[0].strip().lower()
            value = element[1].strip()

            if type == 'id':
                elem = self.driver.find_elements_by_id(value)
            elif type == 'name':
                elem = self.driver.find_elements_by_name(value)
            elif type == 'class':
                elem = self.driver.find_elements_by_class_name(value)
            elif type == 'css':
                elem = self.driver.find_elements_by_css_selector(value)
            elif type == 'tag':
                elem = self.driver.find_elements_by_tag_name(value)
            elif type == 'link_text':
                elem = self.driver.find_elements_by_link_text(value)
            elif type == 'xpath':
                elem = self.driver.find_elements_by_xpath(value)
            else:
                raise NameError("Please correct the type in function parameter.")
        except Exception:
            raise ValueError("No such element found "+str(element))
        return elem

    def open(self,url):
        pure_url = url.strip()
        if pure_url:
            self.driver.get(pure_url)
        else:
            raise ValueError("Please provide a base URL.")

    def type_text(self,element,value):
        element.send_keys(value)

    def enter(self,element):
        element.send_keys(Keys.ENTER)

    def click(self,element):
        element.click()

    def quit(self):
        self.driver.quit()

    def getAttribute(self,element,attribute):
        if element and attribute.strip():
            return element.get_attribute(attribute)
        else:
            raise ValueError("Invalid parameter for getAttribute() invoke.")

    def getText(self,element):
        return element.Text

    def clearText(self,element):
        element.clear()

    def getTitle(self):
        return self.driver.title

    def getCurrentUrl(self):
        return self.driver.current_url

    def getScreenshot(self,targetpath):
        if os.path.exists(targetpath):
            self.driver.get_screenshot_as_file(targetpath)
        else:
            raise IOError("Specified path does not exist.")

    def maximizeWindow(self):
        self.driver.maximize_window()

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def getWindowSize(self):
        return self.driver.get_window_size()

    def refresh(self):
        self.driver.refresh()
        self.driver.switch_to()