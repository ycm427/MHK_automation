from selenium.common.exceptions import *
from selenium.webdriver.support import ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import *
from MarkerPageCommon import MarkerPageCommon


class ZuowenShiping(MarkerPageCommon):
    def __init__(self,driver):
        self.url='http://10.4.67.141/static/readRoll.html'
        super(ZuowenShiping,self).__init__(driver,self.url)
        try:
            self.text_taskcategory = self.findElement(['xpath', "//div[@class='content-title-img']/span"])
            self.text_currentshowno = self.findElement(['xpath', "//div[@class='content-frame-title-left']/span[@class='code']"])
            self.text_submitamount = self.findElement(['xpath', "//div[@class='content-frame-title-right']/span[1]"])
            self.text_problemamount = self.findElement(['xpath', "//div[@class='content-frame-title-right']/span[2]"])
            self.img_answer_content = self.findElement(['xpath',"//div[@class='composition-content-main']/img"])
            self.score_board = self.findElements(['xpath', "//a[@answer-typt='number']"])
        except Exception,e:
            raise NoSuchElementException("Cannot find the element. "+repr(e))

    def isLoaded_content_image(self):
        try:
            return self.img_answer_content.is_displayed()
        except Exception,e:
            raise NoSuchAttributeException("is_displayed() is invalid method for img_answer_content element. "+repr(e))

    def getImage_URL(self):
        return self.getAttribute(self.img_answer_content,"src")

    def score(self,value):
        # return True stands for score successfully, return False stands for operation failed.
        try:
            for eachscore in self.score_board:
                if str(value) == eachscore.text:
                    self.click(eachscore)
                    #self.locate_elements()
                    return True
            raise ValueError("Provided score value is not available in score board.")
            return False
        except Exception,e:
            raise ValueError("Exception occurred while scoring. "+repr(e))

    def getText_Test_Category(self):
        try:
            return self.getAttribute(self.text_taskcategory,"innerHTML")
        except Exception,e:
            print e

    def click_task(self,index=1):
        try:
            self.click(self.task_list[index].find_element_by_xpath("./td[1]"))
            ui.WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='composition-content-main']/img")))
        except IndexError,e1:
            raise IndexError("The index is not accepted. "+repr(e1))
        except Exception,e2:
            raise Exception("Click the task failed. "+repr(e2))

class ZuowenZhengping(ZuowenShiping):
    def __init__(self,driver):
        super(ZuowenZhengping,self).__init__(driver)
        try:
            self.radio_problem = self.findElement(['xpath',"//div[@id='conversation']/div[@class='js-radios']/div[1]"])
            self.radio_blank = self.findElement(['xpath',"//div[@id='conversation']/div[@class='js-radios']/div[2]"])
        except Exception,e:
            raise NoSuchElementException(e.message)

    def mark_problem(self):
        try:
            self.click(self.radio_problem)
        except Exception,e:
            raise NoSuchAttributeException(e.message)

    def mark_blank(self):
        try:
            self.click(self.radio_blank)
        except Exception,e:
            raise NoSuchElementException(e.message)




