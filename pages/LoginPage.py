#coding=utf-8

from time import sleep
from BasePage import BasePage
from selenium.webdriver.support import ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import *


class AnyEc(object):
    def __init__(self,*args):
        self.ecs = args

    def __call__(self,driver):
        for fn in self.ecs:
            try:
                if fn(driver):
                    return True
            except:
                print "Exception occurred"


class LoginPage(BasePage):

    # Locate all web elements via BasePage methods
    def __init__(self,driver):
        super(LoginPage,self).__init__(driver)
        self.url = 'http://10.4.67.141/static/login.html'
        self.driver.implicitly_wait(2)
        self.open(self.url)
        self.maximizeWindow()
        try:
            self.input_uname = self.findElement(['id','username'])
            self.input_pwd = self.findElement(['id','password'])
            self.selectbox_role = self.findElement(['class','select_box'])
            self.button_login = self.findElement(['id','login-btn'])
            self.title = self.getTitle()
            self.header = self.findElement(['class','logoLogin'])
            self.subheader = self.findElement(['class','logoRightLogin'])
            self.welcome_text = self.findElement(['class','welcome'])
            self.image_main = self.findElement(['xpath',"//div[@class='main_left']/img"])
            self.warning_msg = self.findElement(['class','warning'])
        except Exception:
            raise ValueError("Cannot locate the element. "+Exception.message)

    # Status checking methods for each element
    def isDisplayed_uname(self):
        return self.input_uname.is_displayed()

    def isDisplayed_pwd(self):
        return self.input_pwd.is_displayed()

    def isDisplayed_role(self):
        return self.selectbox_role.is_displayed()

    def isDisplayed_btnLogin(self):
        return self.button_login.is_displayed()

    def isDisplayed_mainImage(self):
        return self.image_main.is_displayed()

    def isDisplayed_warningMsg(self):
        return self.warning_msg.is_displayed()

    def isEnabled_uname(self):
        return self.input_uname.is_enabled()

    def isEnabled_pwd(self):
        return self.input_pwd.is_enabled()

    def isEnabled_role(self):
        return self.selectbox_role.is_enabled()

    def isEnabled_btnLogin(self):
        return self.button_login.is_enabled()

    # actions against each element
    def set_uName(self,uname):
        try:
            if self.isEnabled_uname():
                self.type_text(self.input_uname,uname)
        except Exception,e:
            raise AttributeError("set value for user name input box failed."+repr(e))

    def clear_uName(self):
        try:
            if self.isEnabled_uname():
                self.clearText(self.input_uname)
        except Exception,e:
            raise AttributeError("clear text method is not supported by this method. "+repr(e))

    def set_pwd(self,pwd):
        try:
            if self.isEnabled_pwd():
                self.type_text(self.input_pwd,pwd)
        except Exception,e:
            raise AttributeError("set value for password input box failed. "+repr(e))

    def clear_pwd(self):
        try:
            if self.isEnabled_pwd():
                self.clearText(self.input_pwd)
        except Exception,e:
            raise AttributeError("clear text method is not supported by this method. "+repr(e))

    def get_roleOptions(self):
        try:
            self.click(self.selectbox_role)
            option_elements = self.selectbox_role.find_elements_by_tag_name('li')
            if option_elements:
                self.role_options = [self.getAttribute(option,'innerHTML') for option in option_elements]
                return self.role_options
            else:
                print "Role option retrieval failed."
                return []
        except Exception,e:
            raise AttributeError("Method is not supported. "+repr(e))

    def select_role(self,value):
        try:
            self.get_roleOptions()
            target_option = value.strip()
            if target_option in self.role_options:
                self.selectbox_role.find_element_by_xpath("./ul/li[@role_name='"+target_option+"']").click()
        except Exception,e:
            raise BaseException("Invalid values for method reference. "+repr(e))

    def get_welcomeText(self):
        return self.getAttribute(self.welcome_text,"innerHTML")

    def get_headerText(self):
        return self.getAttribute(self.header, 'text')

    def get_subheaderText(self):
        return self.getAttribute(self.subheader, 'text')

    def get_placeholder_uName(self):
        return self.input_uname.get_attribute('data-holder')

    def get_placeholder_pwd(self):
        return self.input_pwd.get_attribute('data-holder')

    def get_warning_message(self):
        return self.getAttribute(self.warning_msg,"innerHTML")

    def click_btnLogin(self):
        if self.isDisplayed_btnLogin():
            self.button_login.click()
            sleep(2)
            #ui.WebDriverWait(self.driver, 4).until(AnyEc(EC.presence_of_element_located((By.CLASS_NAME,"popup")),EC.presence_of_element_located((By.CLASS_NAME,"btn-mid"))))

    

