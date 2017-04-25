#coding=utf-8
from BasePage import BasePage
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support import ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import *
from time import sleep


class MarkerPageCommon(BasePage):

    def __init__(self,driver,url):
        super(MarkerPageCommon,self).__init__(driver)
        self.url = url
        self.locate_elements()

    def locate_elements(self):
        try:
            temp = self.findElement(['class','popup'])
            self.task_loaded = False
        except:
            self.task_loaded = True

        try:
            if self.task_loaded:
                self.header_left = self.findElement(['class', 'container-left'])
                self.header_right = self.findElement(['class', 'container-right'])
                self.header_text = self.header_left.text
                self.header_marking_status = self.header_left.find_element_by_tag_name('span')
                self.marker_id = self.header_right.find_element_by_class_name('container-username')
                self.link_quit = self.header_right.find_element_by_class_name('logoutReadRoll')
                self.task_list = self.findElements(['xpath', "//table[@class='taskList']/tbody/tr"])
                self.button_submit = self.findElement(['class', 'btn-mid'])
            else:
                self.window_popup = temp
                self.button_confirm = self.window_popup.find_element_by_class_name('popup-btn-confirm')
                self.text_wincontent = self.window_popup.find_element_by_class_name('popup-text').text
                try:
                    self.button_cancel = self.window_popup.find_element_by_class_name('popup-btn-cancel')
                except:
                    self.button_cancel = None

        except exceptions.NoSuchElementException as e1:
            raise exceptions.NoSuchElementException(e1.msg)
        except exceptions.NoSuchAttributeException as e2:
            raise exceptions.NoSuchAttributeException(e2.msg)
        except exceptions.ElementNotVisibleException as e3:
            raise exceptions.ElementNotVisibleException(e3.msg)
        except Exception,e:
            raise BaseException("General exception. "+repr(e))

    def click_confirm(self):
        try:
            if not self.task_loaded:
                self.click(self.button_confirm)
                ui.WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"sub_num")))
                self.locate_elements()
            else:
                print "Popup is not shown."
        except Exception,e:
            raise exceptions.NoSuchElementException('Confirm button is not visible.')

    def click_cancel(self):
        try:
            if not self.task_loaded and self.button_cancel:
                self.click(self.button_cancel)
                self.locate_elements()
            else:
                print "Popup is not shown OR [Cancel] button is unavailable in the window."
        except Exception,e:
            raise exceptions.NoSuchElementException('Cancel button is not visible.')

    def click_quit(self):
        try:
            self.click(self.link_quit)
        except Exception,e:
            raise Exception("Click quit link button failed. "+repr(e))

    def click_task(self,index=1):
        try:
            self.click(self.task_list[index].find_element_by_xpath("./td[1]"))
            #self.locate_elements()
        except IndexError,e1:
            raise IndexError("The index is not accepted. "+repr(e1))
        except Exception,e2:
            raise Exception("Click the task failed. "+repr(e2))

    def click_submit(self):
        try:
            self.click(self.button_submit)
            sleep(0.5)
            self.locate_elements()
        except Exception,e:
            raise Exception("Click submit button failed. "+repr(e))

    def get_marker_id(self):
        try:
            return self.marker_id.text
        except Exception,e:
            raise exceptions.NoSuchAttributeException(e.message)

    def get_marker_status(self):
        try:
            return self.header_marking_status.text
        except Exception,e:
            raise exceptions.NoSuchAttributeException(e.message)
    
    def get_task_category(self):
        try:
            return self.text_taskcategory.get_attribute("innerHTML")
        except Exception,e:
            raise exceptions.NoSuchAttributeException(e.message)

    def get_currentshowno(self):
        try:
            return self.text_currentshowno.get_attribute("innerHTML")
        except Exception,e:
            raise exceptions.NoSuchAttributeException(e.message)

    def get_submittedamount(self):
        try:
            return self.text_submitamount.get_attribute("innerHTML")
        except Exception,e:
            raise exceptions.NoSuchAttributeException(e.message)

    def get_problemamount(self):
        try:
            return self.text_problemamount.get_attribute("innerHTML")
        except Exception,e:
            raise exceptions.NoSuchAttributeException(e.message)
        
    def get_selected_task_row(self):
        ret = -1
        try:
            if self.task_list:
               for index in range(len(self.task_list)):
                   status = self.getAttribute(self.task_list[index],'class')
                   if 'checking' in status:
                       ret = index
            return ret
        except Exception,e:
            raise Exception("Selected row is not found. "+repr(e))

    def collect_tasklist_data(self):
        task_list_data = []
        try:
            for eachrow in self.task_list:
                record = {}
                first_column = eachrow.find_element_by_xpath("./td[1]")
                second_column = eachrow.find_element_by_xpath("./td[2]")
                record.setdefault('show_no',first_column.text)
                record.setdefault('taskid',self.getAttribute(first_column,'task-id'))
                record.setdefault('markrecordid', self.getAttribute(first_column, 'mark-record-id'))
                record.setdefault('resource_path', self.getAttribute(first_column, 'res_path'))
                record.setdefault('question_type', self.getAttribute(first_column, 'question-type-id'))
                record.setdefault('task_status', self.getAttribute(first_column, 'task-status'))
                record.setdefault('task_type',self.getAttribute(first_column, 'task-type'))
                record.setdefault('question_title', self.getAttribute(first_column, 'question_title'))
                record.setdefault('question_content', self.getAttribute(first_column, 'question_content'))
                record.setdefault('batch_id', self.getAttribute(first_column, 'data-batch-id'))
                record.setdefault('score', second_column.text)
                task_list_data.append(record)
            return task_list_data
        except Exception,e:
            raise Exception("Task list parsing failed. "+repr(e))

    def collect_showno_list(self):
        showno_list = []
        try:
            for eachrow in self.task_list:
                showno_list.append(eachrow.find_element_by_xpath("./td[1]").text)
            return showno_list
        except Exception,e:
            print e


    def isDisplayed_popup(self):
        return not self.task_loaded
        
