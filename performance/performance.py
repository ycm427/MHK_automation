
#from mhk_requests import *
from locust import HttpLocust,TaskSet,task
from locust.exception import StopLocust
from MySQLdb import *
import time
from datetime import datetime
import string
import json
import random
import logging

backup_markers = []

def random_str(randomlength=10):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(randomlength))

def initialize():
    #conn = connect(host='10.4.67.151', port=3306, user='root', password='iflytekmysql', db='mhk_kf_beifen')
    conn = connect(host='10.4.67.151', port=3306, user='root', password='iflytekmysql', db='mhk_miao')
    cursor = conn.cursor(cursors.DictCursor)

    marker_role_id = "c8249e75dec2488f81a4b95404e021a7"
    team_ids = "'683029a26ac94676bd48a6bf249498e4','6911f7b9166b4400826aa42a03d2e704','fcb556764e0742ad939ac90490a83b91'"
    #team_ids = "'683029a26ac94676bd48a6bf249498e4'"

    sql_all_markers = "SELECT em.user_name marker_name,ms.userid marker_id,ms.question_type_id team_id,ur.roleid role_id FROM sys_marker_status ms JOIN sys_exam_marker em ON ms.userid=em.id " \
                      "JOIN sys_user_role ur ON ms.userid=ur.userid WHERE ms.status='1' AND ms.question_type_id IN (%s) AND ur.roleid='%s' ORDER BY ms.question_type_id ASC LIMIT 55"%(team_ids,marker_role_id)

    cursor.execute(sql_all_markers)
    return list(cursor.fetchall())

all_markers = initialize()
print "%d markers queried."%len(all_markers)
# logfile1 = file('checkUndone.csv','w+')
# logfile2 = file('getNewTask.csv','w+')
# logfile3 = file('markSingleTask.csv','w+')
# logfile4 = file('submitTasks.csv','w+')

class ScoreTaskSet(TaskSet):
    def on_start(self):
        self.time_limit = 10
        self.current_tasks = []
        self.group_id = None
        self.marker_id = None

        global all_markers
        global backup_markers
        if len(all_markers) == 0 and len(backup_markers) > 0:
            all_markers = backup_markers
            backup_markers = []

        if all_markers:
            aMarker = all_markers.pop(random.randint(0,len(all_markers)-1))
            print "aMarker in on_start() method: %s"%aMarker
            self.marker_id = aMarker['marker_id']
            self.team_id = aMarker['team_id']
            self.role_id = aMarker['role_id']
            self.marker_name = aMarker['marker_name']
            backup_markers.append(aMarker)

            if not self.login():
                print "[{0}] login failed, sequence will be terminated.".format(self.marker_name)
                raise StopLocust()

    @task
    def entireMarkScenario(self):
        self.checkUnsubmittedTasks()
        if len(self.current_tasks) == 0:
            self.getNewTaskSet()

        if len(self.current_tasks) > 0:
            for each_task in self.current_tasks:

                if each_task['task_status'] == '0':
                    self.scoreSingleTask(each_task['task_id'],each_task['markRecordId'])
                    time.sleep(3)

            self.submitMarkedTasks()
        else:
            print "No task assigned for %s" % self.marker_name

    def login(self):
        # If login successfully, return True; otherwise return False
        try:
            data = r"username={0}&userpwd={1}&role_id={2}&team_id={3}&date={4}".format(self.marker_name,'1',self.role_id,self.team_id,int(round(time.time() * 1000)))
            req = self.client.post('/login/login.do',data=data,headers={'Content-Type':'application/x-www-form-urlencoded'},name='LOGIN')
            if req.status_code == 200:
                original_data = req.json()
                if original_data['status'] == '1':
                    print "Login successfully.[{0}]".format(self.marker_name)
                    return True
                else:
                    print "Login failed.[{0}]".format(self.marker_name)
                    return False
            else:
                print "Login failed.[{0}]".format(self.marker_name)
                return False

        except Exception as e:
            print "ERROR occurred in [{0}] login. Error meesage: {1}".format(self.marker_name,e.message)
            return False

    def checkUnsubmittedTasks(self):
        try:
            self.current_tasks = []
            payload = {'user_id':self.marker_id,'team_id':self.team_id,'role_id':self.role_id,'date':int(round(time.time() * 1000)),'_':int(round(time.time() * 1000))}
            start = datetime.now()
            req = self.client.get('/task/checkUndoneTask.do',params=payload,name='CHECK')
            print "Request [%s] executed."%req.url
            print "STATUS_CODE: {0}".format(req.status_code)
            elipsed = datetime.now()-start
            #logfile1.write(req.url+','+str(req.status_code)+','+ str(start) +','+str(elipsed)+'\n')

            if req.status_code == 200:
                result = json.loads(req.text)
                if result['status'] == '1':
                    data_set = result['data']
                    if data_set:
                        if data_set['group_id']:
                            self.group_id = data_set['group_id']
                        if len(data_set['task_list'])>0:
                            self.current_tasks = data_set['task_list']
                    else:
                        print "No data body available.[checkUnsubmittedTasks]"
            else:
                print "Request [checkUnsubmittedTasks] executed failed. STATUS CODE:%d"%req.status_code
        except Exception as exp:
            print "ERROR occurred in [checkUnsubmittedTasks]:%s" %exp

    def getNewTaskSet(self):
        try:
            payload = {'user_id': self.marker_id, 'team_id': self.team_id, 'role_id': self.role_id,'date': str(int(time.time())), '_': random_str(12)}
            start = datetime.now()
            req = self.client.get('/task/getNewGroupTask.do', params=payload,name='RETRIEVE')
            print "Request [%s] executed." % req.url
            print "STATUS_CODE: {0}".format(req.status_code)
            elipsed = datetime.now() - start
            #logfile2.write(req.url + ',' + str(req.status_code) + ',' + str(start) + ',' + str(elipsed) + '\n')
            if req.status_code == 200:
                result = json.loads(req.text)
                if result['status'] == '1':
                    data_set = result['data']
                    if data_set:
                        if data_set['group_id']:
                            self.group_id = data_set['group_id']
                        if data_set['task_list']:
                            self.current_tasks = data_set['task_list']
                    else:
                        print "No data body available.[getNewTaskSet]"
            else:
                print "Request [getNewTaskSet] executed failed."
        except Exception as exp:
            print "ERROR occurred in [getNewTaskSet]:%s" %exp

    def scoreSingleTask(self,task_id,mark_record_id):
        try:
            payload = {'user_id':self.marker_id,'role_id':self.role_id,'_':random_str(12)}
            payload.setdefault('task_id',task_id)
            payload.setdefault('mark_record_id', mark_record_id)
            payload.setdefault('time_limit', self.time_limit)
            score = random.choice('0123456N23456P')
            payload.setdefault('task_score', score)
            time_consumed = random.randrange(self.time_limit + 1, self.time_limit + 16, 1)
            payload.setdefault('mark_time', time_consumed)

            start = datetime.now()
            req = self.client.get('/task/updateTask.do',params=payload,name='SCORE')
            print "Request [%s] executed." % req.url
            print "STATUS_CODE: {0}".format(req.status_code)
            elipsed = datetime.now()-start
            #logfile3.write(req.url + ',' + str(req.status_code) + ',' + str(start) + ',' + str(elipsed) + '\n')
            return req.status_code

        except Exception as e:
            print "ERROR occurred in [scoreSingleTask]:%s"%e
            print "[task_id]%s,[mark_record_id]%s"%(task_id,mark_record_id)
            return -1

    def submitMarkedTasks(self):
        try:
            payload = {'user_id': self.marker_id, 'team_id': self.team_id, 'role_id': self.role_id,'group_id': self.group_id, 'time_limit': self.time_limit}
            payload.setdefault('task_score',random.choice('013233445456'))
            payload.setdefault('mark_time',random.randrange(self.time_limit + 1, self.time_limit + 16, 1))
            payload.setdefault('_', random_str(12))
            payload.setdefault('mark_record_id',self.current_tasks[-1]['markRecordId'])
            payload.setdefault('task_id', self.current_tasks[-1]['task_id'])
            payload.setdefault('date', str(int(time.time())))

            start = datetime.now()
            req = self.client.get("/task/subTaskList.do", params=payload,name='SUBMIT')
            print "Request [%s] executed." % req.url
            print "STATUS_CODE: {0}".format(req.status_code)
            elipsed = datetime.now()-start
            #logfile4.write(req.url + ',' + str(req.status_code) + ',' + str(start) + ',' + str(elipsed) + '\n')

        except Exception as e:
            print "ERROR occurred in [submitMarkedTasks]:%s" % e


class performanceMhk(HttpLocust):
    task_set = ScoreTaskSet
    host = 'http://10.4.67.141:18081/mhk'
    min_wait = 500
    max_wait = 1000



