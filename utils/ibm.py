import logging
import os
import threading
import time

def generate_iam_token():
    logging.info('[GENERATE] Generando IAM Token')
    get_iam_token()
    logging.info('[GENERATE] Token creado')

def get_iam_token():
    import requests

    try:
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = { "Content-Type" : "application/x-www-form-urlencoded" }
        data = "apikey=" + os.environ.get("WATSONAPIKEY") + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        response = requests.post( url, headers=headers, data=data )
        iam_token = response.json()["access_token"]
        os.environ['IAM_TOKEN'] = iam_token

    except:
        logging.error('[GENERATE] Error obteniendo Token IAM; reintentando')
        time.sleep(5)
        generate_iam_token()

class ThreadJob(threading.Thread):
    def __init__(self,callback,event,interval):
        '''runs the callback function after interval seconds

        :param callback:  callback function to invoke
        :param event: external event for controlling the update operation
        :param interval: time in seconds after which are required to fire the callback
        :type callback: function
        :type interval: int
        '''
        self.callback = callback
        self.event = event
        self.interval = interval
        super(ThreadJob,self).__init__()

    def run(self):
        while not self.event.wait(self.interval):
            self.callback()