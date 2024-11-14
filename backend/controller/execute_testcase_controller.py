import json

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


# 执行测试用例的任务
def task_execute_testcase(case_id):
    with app.app_context():  # 推送应用上下文
        case_data = TestCaseModel.query.filter(TestCaseModel.id == case_id, TestCaseModel.isDeleted == 0).first()

        case_data = case_data.__dict__
        method = case_data['method']
        protocol = case_data['protocol']
        host = case_data['host']
        port = case_data['port']
        path = case_data['path']
        params = json.loads(case_data['params'])
        headers = case_data['headers']
        payload = case_data['body']
        predict = case_data['predict']

        url = f'{protocol}://{host}:{port}/{path}'
        response = requests.request(method=method, url=url, params=params, headers=headers, json=payload)
        app.logger.info(response.json())

        return response.json()


# 使用线程池执行用例
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
        app.logger.info('需要执行的测试用例编号列表为: {}'.format(caseid_list))
        valid_caseid_list = []
        for case_id in caseid_list:
            case_data = TestCaseModel.query.filter(TestCaseModel.id == case_id, TestCaseModel.isDeleted == 0).first()
            if (not case_data) or case_data.suite.isDeleted or case_data.suite.project.isDeleted:
                # app.logger.info('case_id为{}的测试用例在数据库中查询不到'.format(case_id))
                continue
            valid_caseid_list.append(case_data.id)
        mult_thread(poolsize=POOL_SIZE, caseid_list=valid_caseid_list, callback=cls.collection_results)

    @classmethod
    def collection_results(cls, *args, **kwargs):
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

        result = ExecuteTestcaseController.execute_testcase(request.get_json())
        app.logger.info(result)
        return make_response(CodeUtil.SUCCESS, data=result)
