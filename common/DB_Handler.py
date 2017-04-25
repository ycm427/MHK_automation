#coding=utf-8

import MySQLdb
from collections import *
from tabulate import tabulate

class dataQuery(object):
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='10.4.67.151', port=3306, user='root', password='iflytekmysql', db='mhk_kf_beifen',use_unicode=True, charset='utf8')
            self.conn.autocommit(True)
            self.cursor = self.conn.cursor()
            # self.ZUOWEN_ID = None
            # self.TIANKONG_ID = None
            # self.WENTIYI_ID = None
            # self.WENTIER_ID = None

            self.getStaticData()
        except Exception,e:
            raise MySQLdb.MySQLError("Get DB connection failed, please check DB config."+e.message)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def getStaticData(self):
        self.ZUOWEN_ID = self.getQuestionID_Zuowen()
        self.TIANKONG_ID = self.getQuestionID_Tiankong()
        self.WENTIYI_ID = self.getQuestionID_Wentiyi()
        self.WENTIER_ID = self.getQuestionID_Wentier()
        self.ROLE_ID_YUEJUAN = self.getRoleID_Yuejuan()
        self.ROLE_ID_FUPING = self.getRoleID_Fuping()
        self.ROLE_ID_DAZUZHANG = self.getRoleID_Dazuzhang()
        self.ROLE_ID_XIAOZUZHANG = self.getRoleID_Xiaozuzhang()

    def getQuestionID_Zuowen(self):
        try:
            sql = "SELECT id FROM sys_question_type WHERE enable_flg='1' AND name IN ('作文','读后写')"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getQuestionID_Tiankong(self):
        try:
            sql = "SELECT id FROM sys_question_type WHERE enable_flg='1' AND name IN ('填空','听后写')"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getQuestionID_Wentiyi(self):
        try:
            sql = "SELECT id FROM sys_question_type WHERE enable_flg='1' AND name IN ('问题一','复述')"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getQuestionID_Wentier(self):
        try:
            sql = "SELECT id FROM sys_question_type WHERE enable_flg='1' AND name IN ('问题二','选择性回答')"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getRoleID_Yuejuan(self):
        try:
            sql = "SELECT id FROM sys_role WHERE enable_flg='1' AND role_name='阅卷老师'"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getRoleID_Fuping(self):
        try:
            sql = "SELECT id FROM sys_role WHERE enable_flg='1' AND role_name='复评老师'"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getRoleID_Dazuzhang(self):
        try:
            sql = "SELECT id FROM sys_role WHERE enable_flg='1' AND role_name='大组长'"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getRoleID_Xiaozuzhang(self):
        try:
            sql = "SELECT id FROM sys_role WHERE enable_flg='1' AND role_name='小组长'"
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0]
            else:
                return None
        except Exception,e:
            print e
            return None

    def getShiping_By_Type_and_Group(self,type,groupid=1):
        try:
            type_lower = type.lower()
            if (isinstance(groupid,(int,long)) and groupid>=1 and groupid<=3) and (type_lower in ('zw','wty','wte')):
                if type_lower == 'zw':
                    question_type_id = self.ZUOWEN_ID
                elif type_lower == 'wty':
                    question_type_id = self.WENTIYI_ID
                else:
                    question_type_id = self.WENTIER_ID

                sql = "SELECT id,task_id,CONVERT(show_no,char) show_no,batch_order,expert_score,question_id,question_title,question_content,res_path FROM task_test " \
                      "WHERE task_type='2' AND enable_flg='1' AND question_type_id='{0}' AND batch_index={1} ORDER BY batch_order ASC".format(question_type_id,groupid)
                self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
                self.cursor.execute(sql)
                res = self.cursor.fetchall()
                return [item for item in res]
            else:
                raise ValueError("Provided parameters are not invalid, groupid should be INTEGER[1,3], type should be one of (zw,wty,wte)")
        except Exception,e:
            print e
            return None

    def getMarkInterval_By_MarkID(self,markerid):
        try:
            if not isinstance(markerid,basestring):
                raise TypeError("String type marker ID is required.")
            else:
                sql_marker_id = "SELECT id FROM sys_exam_marker WHERE user_status='1' AND enable_flg='1' AND user_name='{0}'".format(markerid)
                self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
                self.cursor.execute(sql_marker_id)
                marker_dbID = self.cursor.fetchone()
                if marker_dbID:
                    sql_interval_1 = "SELECT CONVERT(diff_time,UNSIGNED) diff_time FROM sys_diff_time WHERE exam_marker_id='{0}'".format(marker_dbID[0])
                    self.cursor.execute(sql_interval_1)
                    interval1 = self.cursor.fetchone()
                    if interval1:
                        return interval1[0]
                    else:
                        sql_interval_2 = "SELECT mark_time FROM sys_question_type WHERE id=(SELECT question_type_id FROM sys_marker_status WHERE userid='{0}');".format(marker_dbID[0])
                        self.cursor.execute(sql_interval_2)
                        interval2 = self.cursor.fetchone()
                        if interval2:
                            return interval2[0]
                        else:
                            return 60
                else:
                    raise ValueError("Provided marker is not valid.")
        except Exception,e:
            print e

    def getRandomMarkerID_Zuowen_no_Shiping_Tasks_Loaded(self):
        try:
            sql_random_marker_dbid = "SELECT userid FROM sys_marker_status WHERE question_type_id='{0}' AND status='0' AND userid NOT IN " \
                                     "(SELECT DISTINCT marker_id FROM mark_record WHERE task_type='2' AND question_type_id='{0}' " \
                                    "GROUP BY marker_id,mark_status HAVING mark_status IN ('0','1')) ORDER BY RAND() LIMIT 1".format(self.ZUOWEN_ID,self.ZUOWEN_ID)
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql_random_marker_dbid)
            marker_dbid = self.cursor.fetchone()[0]
            return marker_dbid
        except Exception,e:
            print e

    def getRandomMarkerID_Zuowen_Eixsting_Shiping_Tasks(self):
        try:
            sql_random_marker_dbid = "SELECT DISTINCT marker_id FROM mark_record WHERE task_type='2' AND question_type_id='{0}' " \
                                     "GROUP BY marker_id,mark_status HAVING mark_status IN ('0','1') ORDER BY RAND() LIMIT 1".format(self.ZUOWEN_ID)
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql_random_marker_dbid)
            marker_dbid = self.cursor.fetchone()[0]
            return marker_dbid
        except Exception,e:
            print e

    def getRandomMarkerId_Zuowen_Existing_Unscored_Shiping_Tasks(self):
        try:
            sql_random_marker_dbid = "SELECT marker_id FROM mark_record WHERE task_type='2' AND question_type_id='{0}' AND mark_status='0' " \
                                     "GROUP BY marker_id ORDER BY RAND() LIMIT 1".format(self.ZUOWEN_ID)
            self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
            self.cursor.execute(sql_random_marker_dbid)
            marker_dbid = self.cursor.fetchone()[0]
            return marker_dbid
        except Exception,e:
            print e

    def getShipingTaskStatus_By_qType_MarkerId_ShowNo(self,qtypeid,markerid,showno):
        try:
            if qtypeid not in [self.ZUOWEN_ID,self.WENTIYI_ID,self.WENTIER_ID]:
                raise ValueError("Question type id does not exist.")
            if not isinstance(showno,basestring):
                raise TypeError("Assigned show No is not string type.")
            if not isinstance(markerid,basestring):
                raise TypeError("Assigned marker ID is not string type.")
            sql = "SELECT task_id,marker_id,mark_status,score FROM mark_record WHERE task_type='2' AND question_type_id='{0}'" \
                  " AND marker_id='{1}' AND show_no={2}".format(qtypeid,markerid,showno)
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception,e:
            print e


    def getBatchNo_ZuowenShiping_Should_Be_Loaded_By_MarkerId(self,markerid):
        try:
            if isinstance(markerid,basestring):
                sql = "SELECT  group_id,MAX(mark_status) max_status FROM mark_record WHERE task_type='2' AND question_type_id='{0}' AND marker_id='{1}' " \
                      "GROUP BY group_id ORDER BY group_id DESC LIMIT 1".format(self.ZUOWEN_ID,markerid)
                self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
                self.cursor.execute(sql)
                record = self.cursor.fetchone()
                if not record:
                    return 1
                else:
                    max_status = record['max_status']
                    group_id = int(record['group_id'])
                    if max_status == '2':
                        if group_id < 3:
                            return group_id + 1
                        elif group_id == 3:
                            print "This marker had been passed shiping"
                            return 0
                        else:
                            raise ValueError("group_id is assigned with illegal value")
                    elif max_status in ('0','1'):
                        return group_id
                    else:
                        raise ValueError("mark_status is assigned with illegal value")
            else:
                raise TypeError("marker ID is string type required.")
        except Exception,e:
            print e

    def getMarker_loginID_By_DbID(self,dbid):
        try:
            if isinstance(dbid,basestring):
                sql = "SELECT user_name FROM sys_exam_marker WHERE id='{0}'".format(dbid)
                self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
                self.cursor.execute(sql)
                return self.cursor.fetchone()[0]
            else:
                raise TypeError("getMarker_loginID_By_DbID() required string parameter")
        except Exception,e:
            print e

    def getMarker_Realname_By_loginID(self,loginid):
        try:
            if isinstance(loginid,basestring):
                sql = "SELECT real_name FROM sys_exam_marker WHERE user_name='{0}'".format(loginid)
                self.cursor = self.conn.cursor(MySQLdb.cursors.Cursor)
                self.cursor.execute(sql)
                return self.cursor.fetchone()[0]
            else:
                raise TypeError("getMarker_login_Realname_By_loginID() required string parameter")
        except Exception,e:
            print e

    def getZuowenShipingInfo_By_Show_No(self,showno):
        try:
            if isinstance(showno,basestring):
                sql = "SELECT test_number,question_id,batch_index,batch_order,expert_score,res_path FROM task_test " \
                      "WHERE task_type='2' AND question_type_id='{0}' AND show_no='{1}'".format(self.ZUOWEN_ID,showno)
                self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
                self.cursor.execute(sql)
                return self.cursor.fetchone()
            else:
                raise TypeError("getTask_ResPath_By_Show_No() required string parameter")
        except Exception,e:
            print e



# test = dataQuery()
# print test.getBatchNo_ZuowenShiping_Should_Be_Loaded_By_MarkerId('1b1e454ae0a24558a6502ca57997eddf')