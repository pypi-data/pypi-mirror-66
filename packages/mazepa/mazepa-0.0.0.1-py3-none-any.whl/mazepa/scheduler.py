import time
import taskqueue

import boto3
import tenacity

class Scheduler:
    def __init__(self, queue_name=None, threads=1):
        self.queue_name = queue_name
        self.threads = threads


    def execute(self):
        pass

    '''

    '''
    def register_job(self, job):
        pass

    def unregister_job(self):
        pass

