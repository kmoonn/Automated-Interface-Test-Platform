import requests
import threadpool
from flask import request
from flask_restful import Resource

from backend.app import app
from backend.config import POOL_SIZE
from backend.models.test_case_model import TestCaseModel
from backend.utils.code_utils import CodeUtil
from backend.utils.exception_utils import REQ_IS_EMPTY_ERROR, REQ_TYPE_ERROR, REQ_KEY_ERROR
from backend.utils.make_response_utils import make_response


def task_execute_testcase(caseid):
    case_data = TestCaseModel.query.filter(TestCaseModel.id == caseid, TestCaseModel.isDeleted == 0).first()

    method = case_data['method']
    protocol = case_data['protocol']
    host = case_data['host']
    port = case_data['port']
    path = case_data['path']
    params = case_data['params']
    headers = case_data['headers']
    payload = case_data['body']
    predict = case_data['predict']

    url = f'{protocol}://{host}:{port}/{path}'
    response = requests.request(method=method, url=url, params=params, headers=headers, json=payload)
    app.logger.info(response.text)

    return response.json()


def mult_thread(poolsize=5, caseid_list=None, callback=None):
    pool = threadpool.ThreadPool(poolsize)
    req_list = threadpool.makeRequests(task_execute_testcase, caseid_list, callback)
    [pool.putRequest(req) for req in req_list]
    pool.wait()


class ExecuteTestcaseController(Resource):
    response_list = []

    @classmethod
    def execute_testcase(cls, testcase_data):
        caseid_list = testcase_data.get('caseid_list')
        app.logger.info('ExecuteTestcase: caseid_list={}'.format(caseid_list))
        valid_caseid_list = []
        for caseid in caseid_list:
            case_data = TestCaseModel.query.filter(TestCaseModel.id == caseid, TestCaseModel.isDeleted == 0).first()
            if not case_data or not case_data.suite.isDeleted or not case_data.suite.projetc.isDeleted:
                app.logger.info('ExecuteTestcase: caseid={} is invalid'.format(caseid))
                continue
            valid_caseid_list.append(case_data.id)
        mult_thread(poolsize=POOL_SIZE, caseid_list=valid_caseid_list, callback=cls.collection_results())

    @classmethod
    def collection_results(cls, *args):
        result = args[1]
        cls.response_list.append(result)


class ExecuteTestcaseService(Resource):
    def post(self):
        if not request.data:
            raise REQ_IS_EMPTY_ERROR()
        if not request.is_json:
            raise REQ_TYPE_ERROR()
        caseid_list = request.json.get('caseid_list')
        if not caseid_list:
            raise REQ_KEY_ERROR()
        if len(caseid_list) < 1:
            raise ValueError()

        ExecuteTestcaseController.execute_testcase(request.get_json())
        return make_response(CodeUtil.SUCCESS, data=ExecuteTestcaseController.response_list)
