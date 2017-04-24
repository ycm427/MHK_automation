#coding=utf-8

import os
import sys
from datetime import datetime
from time import sleep
import HTMLTestRunner
from selenium import webdriver
import unittest
from LoginPage import LoginPage
from Zuowen import ZuowenShiping
from DB_Handler import dataQuery


path = os.getcwd()
parent = os.path.dirname(path)


class tc_zuowen_shiping_task_load(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.db = dataQuery()

    def tearDown(self):
        if sys.exc_info()[0]:
            test_method_name = self._testMethodName
            fname = '_'.join([test_method_name, datetime.now().strftime("%Y%m%d%H%M%S.png")])
            screenshot_folder = os.sep.join([parent,'screenshots'])
            if not os.path.exists(screenshot_folder):
                os.mkdir(screenshot_folder)
            self.driver.save_screenshot(os.sep.join([screenshot_folder,fname]))
        self.driver.quit()

    def test_01_tasks_confirm_load(self):
        pageLogin = LoginPage(self.driver)
        # 随机获取未分配试评任务的阅卷老师登录ID
        q_marker_db_id = self.db.getRandomMarkerID_Zuowen_no_Shiping_Tasks_Loaded()
        q_marker_login_id = self.db.getMarker_loginID_By_DbID(q_marker_db_id)
        q_should_load_shiping_batchNo = self.db.getBatchNo_ZuowenShiping_Should_Be_Loaded_By_MarkerId(q_marker_db_id)
        if q_should_load_shiping_batchNo == 0:
            # 当选中阅卷老师已通过试评时，引出失败断言来终止继续执行
            self.assertEqual(0, 1, "This marker had been passed Zuowen Shiping")
        pageLogin.set_uName(q_marker_login_id)
        pageLogin.set_pwd('1')
        pageLogin.select_role(u'阅卷老师')
        pageLogin.click_btnLogin()

        pageShiping = ZuowenShiping(self.driver)
        # 获取任务确认框应弹出
        self.assertTrue(pageShiping.isDisplayed_popup(),"Popup is NOT shown.")
        pageShiping.click_confirm()
        # 显示的用户名应与登录名一致
        self.assertEqual(pageShiping.get_marker_id(), q_marker_login_id,"Shown marker ID is not identical with the actual one.")
        # 应显示“试评”
        self.assertEqual(pageShiping.get_marker_status(),u"试评","Should shown SHIPING")
        # 应显示“作文”
        self.assertEqual(pageShiping.getText_Test_Category(),u"作文","Should shown ZUOWEN")
        # 应获取10个试评任务
        self.assertEqual(len(pageShiping.task_list),10)
        actual_shownolist = pageShiping.collect_showno_list()
        expected_tasklist = self.db.getShiping_By_Type_and_Group('ZW',q_should_load_shiping_batchNo)
        for expected_each in expected_tasklist:
            self.assertIn(expected_each['show_no'],actual_shownolist,"{0} not found in actual show NO list".format(expected_each['show_no']))

        pageShiping.click_quit()

    def test_02_tasks_cancel_load(self):
        pageLogin = LoginPage(self.driver)
        # 随机获取未分配试评任务的阅卷老师登录ID
        q_marker_db_id = self.db.getRandomMarkerID_Zuowen_no_Shiping_Tasks_Loaded()
        q_marker_login_id = self.db.getMarker_loginID_By_DbID(q_marker_db_id)
        q_should_load_shiping_batchNo = self.db.getBatchNo_ZuowenShiping_Should_Be_Loaded_By_MarkerId(q_marker_db_id)
        if q_should_load_shiping_batchNo == 0:
            # 当选中阅卷老师已通过试评时，引出失败断言来终止继续执行
            self.assertEqual(0, 1, "This marker had been passed Zuowen Shiping")
        pageLogin.set_uName(q_marker_login_id)
        pageLogin.set_pwd('1')
        pageLogin.select_role(u'阅卷老师')
        pageLogin.click_btnLogin()

        pageShiping = ZuowenShiping(self.driver)
        # 获取任务确认框应弹出
        self.assertTrue(pageShiping.isDisplayed_popup(),"Popup is NOT shown.")
        pageShiping.click_cancel()

        # 内容栏显示“暂无数据”
        self.assertEqual(pageShiping.driver.find_element_by_xpath("//div[@class='content-empty']/h2").text,u"暂无数据")
        self.assertEqual(len(pageShiping.task_list),0)

        pageShiping.click_quit()

    def test_03_tasks_exists(self):
        pageLogin = LoginPage(self.driver)
        # 随机获取已分配试评任务的阅卷老师登录ID
        q_marker_db_id = self.db.getRandomMarkerID_Zuowen_Eixsting_Shiping_Tasks()
        q_marker_login_id = self.db.getMarker_loginID_By_DbID(q_marker_db_id)
        q_should_load_shiping_batchNo = self.db.getBatchNo_ZuowenShiping_Should_Be_Loaded_By_MarkerId(q_marker_db_id)
        if q_should_load_shiping_batchNo == 0:
            # 当选中阅卷老师已通过试评时，引出失败断言来终止继续执行
            self.assertEqual(0, 1, "This marker had been passed Zuowen Shiping")

        pageLogin.set_uName(q_marker_login_id)
        pageLogin.set_pwd('1')
        pageLogin.select_role(u'阅卷老师')
        pageLogin.click_btnLogin()

        pageShiping = ZuowenShiping(self.driver)
        # 获取任务确认框不应弹出
        self.assertFalse(pageShiping.isDisplayed_popup())
        # 显示的用户名应与登录名一致
        self.assertEqual(pageShiping.get_marker_id(), q_marker_login_id)
        # 应显示“试评”
        self.assertEqual(pageShiping.get_marker_status(), u"试评")
        # 应显示“作文”
        self.assertEqual(pageShiping.getText_Test_Category(), u"作文")
        # 应获取10个试评任务
        self.assertEqual(len(pageShiping.task_list), 10)
        actual_shownolist = pageShiping.collect_showno_list()
        expected_tasklist = self.db.getShiping_By_Type_and_Group('ZW', q_should_load_shiping_batchNo)
        for expected_each in expected_tasklist:
            self.assertIn(expected_each['show_no'], actual_shownolist,"{0} not found in actual show NO list".format(expected_each['show_no']))

        pageShiping.click_quit()


class tc_zuowen_shiping_data_consistancy(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.db = dataQuery()

    def tearDown(self):
        if sys.exc_info()[0]:
            test_method_name = self._testMethodName
            fname = '_'.join([test_method_name, datetime.now().strftime("%Y%m%d%H%M%S.png")])
            screenshot_folder = os.sep.join([parent,'screenshots'])
            if not os.path.exists(screenshot_folder):
                os.mkdir(screenshot_folder)
            self.driver.save_screenshot(os.sep.join([screenshot_folder,fname]))
        self.driver.quit()

    def test_data_consistancy(self):
        pageLogin = LoginPage(self.driver)
        q_marker_db_id = self.db.getRandomMarkerID_Zuowen_Eixsting_Shiping_Tasks()
        q_marker_login_id = self.db.getMarker_loginID_By_DbID(q_marker_db_id)
        pageLogin.set_uName(q_marker_login_id)
        pageLogin.set_pwd('1')
        pageLogin.select_role(u'阅卷老师')
        pageLogin.click_btnLogin()

        pageShiping = ZuowenShiping(self.driver)
        actual_showno_list = pageShiping.collect_showno_list()
        loop_counter = task_list_len = len(actual_showno_list)
        index = pageShiping.get_selected_task_row()
        if index < 0:
            raise IndexError("Returned selected row index is incorrect.")

        while loop_counter>0:
            # 选中行的 show No 与试题内容栏显示的一致
            self.assertEqual(actual_showno_list[index],pageShiping.get_currentshowno())
            # 答卷图像加载成功
            self.assertTrue(pageShiping.isLoaded_content_image())
            # 答卷图像 URL 与期待值一致
            self.assertEqual(pageShiping.getImage_URL(),self.db.getZuowenShipingInfo_By_Show_No(actual_showno_list[index])['res_path'])

            loop_counter -= 1
            index = (index+1)%task_list_len
            pageShiping.click_task(index)

suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(tc_zuowen_shiping_task_load))
suite.addTests(unittest.makeSuite(tc_zuowen_shiping_data_consistancy))
unittest.TextTestRunner(verbosity=2)

target_folder = os.sep.join([parent,'reports'])
if not os.path.exists(target_folder):
    os.mkdir(target_folder)
file_name = datetime.now().strftime("%Y%m%d_%H%M%S_report.html")
output = open(os.sep.join([target_folder,file_name]),'w')
runner = HTMLTestRunner.HTMLTestRunner(stream=output,title='MHK marking test report',description=u'作文/读后写题型试评页面的功能测试')
runner.run(suite)
