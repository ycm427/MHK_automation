import os
import requests


def startPerformance(cocurrent_num=10,hatch_rate=2,loglevel='INFO',file_name='performance.py'):
    current_dir = os.path.curdir
    cmdChart = "python {0}".format(os.sep.join([current_dir,'chart.py']))
    cmdLocust = "locust "
    if loglevel in ('DEBUG','INFO','WARNING','ERROR','CRITICAL'):
        cmdLocust += "-L "+loglevel+" "
    else:
        cmdLocust += "-L INFO "
    #cmdLocust += "-f "+os.sep.join([current_dir,file_name])
    cmdLocust += "-f "+file_name
    cmdLocust += " --only-summary --statsfile=result.csv --no-web -c {0} -r {1}".format(cocurrent_num,hatch_rate)
    #cmdLocust += " --no-web -c {0} -r {1}".format(cocurrent_num, hatch_rate)
    cmd1 = os.popen("bokeh serve")
    cmd2 = os.popen(cmdChart)
    #cmd3 = os.popen(cmdLocust)
    #os.system('locust -f performance.py')
    os.system(cmdLocust)

    # response = requests.post('http://127.0.0.1:8089/swarm',{'locust_count':cocurrent_num,'hatch_rate':hatch_rate})
    # print response.status_code

startPerformance(cocurrent_num=50,hatch_rate=4)