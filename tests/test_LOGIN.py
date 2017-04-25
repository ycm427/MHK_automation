#coding=utf-8

import os
import sys
from datetime import datetime
from selenium import webdriver
from unittest import TestCase,TestLoader,TextTestRunner,TestSuite,makeSuite
from LoginPage import LoginPage
from Zuowen import ZuowenShiping,ZuowenZhengping
import HTMLTestRunner


path = os.getcwd()
parent = os.path.dirname(path)


class tc_login_staticCheck(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_staticCheck(self):
        """Check key elements status (visibility, usability, text)"""
        page = LoginPage(self.driver)
        self.assertEqual(page.getTitle(),u"账号登录",u"页面名称不一致")
        self.assertEqual(page.get_headerText(),u"中国少数民族汉语水平等级考试(MHK三级)",u"大标题不一致")
        self.assertEqual(page.get_subheaderText(), u"计算机辅助阅卷平台", u"小标题不一致")
        self.assertTrue(page.isDisplayed_mainImage(),u"图片未加载")
        self.assertEqual(page.get_welcomeText(),u"欢迎参加本次阅卷,请选择角色并点击登录")
        self.assertTrue(page.isEnabled_uname())
        self.assertEqual(page.get_placeholder_uName(),u"请输入账号")
        self.assertTrue(page.isEnabled_pwd())
        self.assertEqual(page.get_placeholder_pwd(),u"请输入密码")
        self.assertTrue(page.isEnabled_role())
        self.assertListEqual(page.get_roleOptions(),[u"请选择"])
        self.assertTrue(page.isDisplayed_btnLogin())
        self.assertFalse(page.isDisplayed_warningMsg())

    def tearDown(self):
        self.driver.quit()


class tc_login_enterNonexistentUserID(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_nonexistentUserId(self):
        """Check username & role option appearance while entering nonexistent marker ID"""
        page = LoginPage(self.driver)
        page.set_uName("dahz146xu")
        # Cannot retrieve corresponding role for nonexistent marker ID
        self.assertListEqual(page.get_roleOptions(), [u"请选择"])
        self.assertEqual(page.get_welcomeText(),u"欢迎参加本次阅卷,请选择角色并点击登录")

    def tearDown(self):
        self.driver.quit()


class tc_login_roleList(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_markerOwnMultipleRoles(self):
        """Validate retrieved role options are correct if entered marker owns single/multiple role(s)"""
        page = LoginPage(self.driver)
        # Marker who owns multiple roles
        page.set_uName('zw0009')
        self.assertListEqual(page.get_roleOptions(),[u"请选择",u"复评老师",u"阅卷老师"])
        # Marker who owns single role
        page.clear_uName()
        page.set_uName('wty0001')
        self.assertListEqual(page.get_roleOptions(), [u"请选择",u"阅卷老师"])


class tc_login_requriedfileds_notfilled(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_all_fields_required(self):
        """Validate all 3 fields must be filled with contents to login, or no response."""
        page = LoginPage(self.driver)
        original_url = page.getCurrentUrl()
        original_welcomeText = page.get_welcomeText()
        original_warningShown = page.isDisplayed_warningMsg()

        page.set_uName('zw0009')
        page.set_pwd('1')
        page.click_btnLogin()

        self.assertEqual(original_url,page.getCurrentUrl())
        self.assertEqual(original_welcomeText,page.get_welcomeText())
        self.assertEqual(original_warningShown,page.isDisplayed_warningMsg())


class tc_login_login_incorrectPwd(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_login_incorrectPwd(self):
        """Validate behavior of login via valid marker ID, incorrect password, correct role"""
        page = LoginPage(self.driver)
        page.set_uName("dzzhang")
        page.set_pwd("testMHK")
        page.select_role(u"大组长")
        page.click_btnLogin()
        self.assertEqual(page.get_welcomeText(),u"欢迎您,大组长!")
        self.assertTrue(page.isDisplayed_warningMsg())
        self.assertEqual(page.get_warning_message(),u"用户名或密码错误")


class tc_login_login_successful(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        if sys.exc_info()[0]:
            test_method_name = self._testMethodName
            fname = '_'.join([test_method_name, datetime.now().strftime("%Y%m%d%H%M%S.png")])
            screenshot_folder = os.sep.join([parent,'screenshots'])
            if not os.path.exists(screenshot_folder):
                os.mkdir(screenshot_folder)
            self.driver.save_screenshot(os.sep.join([screenshot_folder,fname]))
        self.driver.quit()

    def test_login_successful(self):
        """Validate login with accepted parameters, page will navigate to objective page."""
        page = LoginPage(self.driver)
        page.set_uName('zw0008')
        page.set_pwd('1')
        page.select_role(u'阅卷老师')
        page.click_btnLogin()
        # Login successfully, the url & page title should be updated
        self.assertNotIn('login.html',page.getCurrentUrl())
        self.assertNotEqual(page.getTitle(),u'账号登录')


suite = TestSuite()
suite.addTests(makeSuite(tc_login_staticCheck))
suite.addTests(makeSuite(tc_login_enterNonexistentUserID))
suite.addTests(makeSuite(tc_login_roleList))
suite.addTests(makeSuite(tc_login_requriedfileds_notfilled))
suite.addTests(makeSuite(tc_login_login_incorrectPwd))
suite.addTests(makeSuite(tc_login_login_successful))

TextTestRunner(verbosity=2)

target_folder = os.sep.join([parent,'reports'])
if not os.path.exists(target_folder):
    os.mkdir(target_folder)
file_name = datetime.now().strftime("%Y%m%d_%H%M%S_report.html")
output = open(os.sep.join([target_folder,file_name]),'w')
runner = HTMLTestRunner.HTMLTestRunner(stream=output,title='MHK marking test report',description='Testing based on 20170421F2 build')
runner.run(suite)