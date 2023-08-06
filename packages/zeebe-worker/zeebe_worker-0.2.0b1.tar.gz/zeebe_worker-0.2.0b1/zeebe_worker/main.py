from threading import Thread
import json
import time
import logging
import grpc
from zeebe_grpc import gateway_pb2 as zeebe

class ZeebeWorker:

    def __init__(self, stub, worker_name, timeout=5*60*1000, request_timeout=1*60*1000,
                 max_jobs_to_activate=1):
        """Initiate a worker class
        """
        self.stub = stub
        self.worker_name = worker_name
        self.timeout = timeout
        self.request_timeout = request_timeout
        self.max_jobs_to_activate = max_jobs_to_activate

    def subscribe(self, task_type, target, timeout=None, request_timeout=None, max_jobs_to_activate=None):
        timeout = timeout or self.timeout
        request_timeout = request_timeout or self.request_timeout
        max_jobs_to_activate = max_jobs_to_activate or self.max_jobs_to_activate

        if not callable(target):
            target = getattr(self, target)

        Thread(target=self._subscribe, args=[task_type, target], kwargs={
            'timeout': timeout,
            'request_timeout': request_timeout,
            'max_jobs_to_activate': max_jobs_to_activate}) \
        .start()

    def _subscribe(self, task_type, target, timeout, request_timeout, max_jobs_to_activate):
        while True:
            logging.debug(f'Polling for {task_type}')
            try:
                req = zeebe.ActivateJobsRequest(
                        type=task_type,
                        worker=self.worker_name,
                        timeout=timeout,
                        requestTimeout=request_timeout,
                        maxJobsToActivate=max_jobs_to_activate)
                # ActivateJobsResponse returns as a stream, therefore a loop is used
                for resp in self.stub.ActivateJobs(req):
                    for job in resp.jobs:
                        logging.info(f'Handling job: {job.key} in instance: {job.workflowInstanceKey}')
                        try:
                            resp_variables = target(job)
                            if not isinstance(resp_variables, dict):
                                resp_variables = {}
                            complete_job_req = zeebe.CompleteJobRequest(
                                    jobKey=job.key, variables=json.dumps(resp_variables))
                            self.stub.CompleteJob(complete_job_req)
                            logging.info(f'Job handled: {job.key} in instance: {job.workflowInstanceKey}')
                        # Catches every exception (https://docs.python.org/3.6/library/exceptions.html#exception-hierarchy)
                        except BaseException as e:
                            logging.error(repr(e), exc_info=True)
                            fail_job_req = zeebe.FailJobRequest(
                                    jobKey=job.key, errorMessage=repr(e))
                            self.stub.FailJob(fail_job_req)
                            logging.info(f'Job failed: {job.key} in instance: {job.workflowInstanceKey}')
            except grpc.RpcError as e:
                logging.error(f'Cannot subscribe to {task_type}\n' + repr(e))
                time.sleep(10)
