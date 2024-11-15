import datetime
import json
import random
import string
import time

import requests
import threadpool
from flask import request
from flask_restful import Resource
from requests.adapters import HTTPAdapter

from backend.app import app, db
from backend.config import POOL_SIZE
from backend.models.test_case_model import TestCaseModel
from backend.models.test_report_model import TestReportModel
from backend.utils.code_utils import CodeUtil
from backend.utils.exception_utils import REQ_IS_EMPTY_ERROR, REQ_TYPE_ERROR, REQ_KEY_ERROR
from backend.utils.make_response_utils import make_response


# 生成测试报告的ID
def generate_random_str(random_length=32):
    str_list = random.sample(string.digits + string.ascii_letters, random_length - 13)
    random_str = ''.join(str_list)
    random_str = str(int(time.time() * 1000)) + random_str
    return random_str


# 断言
def assert_testcase(predict, response):
    if predict == response:
        return True
    else:
        return False


# 执行测试用例的任务
def task_execute_testcase(case_id):
    with app.app_context():
        start_time = datetime.datetime.now()
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

        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=3))
        session.mount('https://', HTTPAdapter(max_retries=3))
        response = session.request(method=method, url=url, params=params, headers=headers, json=payload)
        end_time = datetime.datetime.now()
        time_delta = str((end_time - start_time).total_seconds())

        assert_result = assert_testcase(predict, response)
        if assert_result:
            test_result = "通过"
        else:
            test_result = "失败"

        report_detail = {
            "case_id": case_data.id,
            "case_name": case_data.case_name,
            "suite_id": case_data.suite_id,
            "suite_name": case_data.suite.suite_name,
            "methods": case_data.method,
            "url": response.url,
            "headers": case_data.headers,
            "body": case_data.body,
            "response_data": response.text,
            "status_code": response.status_code,
            "predict": case_data.predict,
            "assert_result": assert_result,
            "test_result": test_result,
            "overtime": time_delta,
        }

        return report_detail


# 使用线程池执行用例
def mult_thread(pool_size=5, case_id_list=None, callback=None):
    pool = threadpool.ThreadPool(pool_size)
    req_list = threadpool.makeRequests(task_execute_testcase, case_id_list, callback)
    [pool.putRequest(req) for req in req_list]
    pool.wait()


class ExecuteTestcaseController(Resource):
    response_list = []

    @classmethod
    def execute_testcase(cls, test_case_data):
        start_time = datetime.datetime.now()
        case_id_list = test_case_data.get('case_id_list')
        valid_case_id_list = []
        for case_id in case_id_list:
            case_data = TestCaseModel.query.filter(TestCaseModel.id == case_id, TestCaseModel.isDeleted == 0).first()
            if (not case_data) or case_data.suite.isDeleted or case_data.suite.project.isDeleted:
                continue
            valid_case_id_list.append(case_data.id)
        mult_thread(pool_size=POOL_SIZE, case_id_list=valid_case_id_list, callback=cls.collection_results)
        end_time = datetime.datetime.now()
        time_delta = str((end_time - start_time).total_seconds())
        report_name = report_id = generate_random_str()
        case_count = len(cls.response_list)
        pass_count = 0
        fail_count = 0
        conclusion = "通过"
        for response_case_data in cls.response_list:
            if response_case_data.get("assert_result"):
                pass_count += 1
            else:
                fail_count += 1
                conclusion = "失败"
        rate = pass_count / case_count

        test_report = {
            "report_name": report_name,
            "report_id": report_id,
            "project_name": test_case_data.get("project_name"),
            "project_id": test_case_data.get("project_id"),
            "case_count": case_count,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "rate": rate,
            "conclusion": conclusion,
            "total_time": time_delta,
            "created_at": datetime.datetime.now(),
            "case_data": str(cls.response_list)
        }

        test_report_data = TestReportModel(**test_report)
        db.session.add(test_report_data)
        db.session.commit()
        db.session.close()

        return cls.response_list

    @classmethod
    def execute_casesuite(cls, test_suite_data):
        pass

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
        case_id_list = request.json.get('case_id_list')
        if not case_id_list:
            raise REQ_KEY_ERROR()
        if len(case_id_list) < 1:
            raise ValueError()

        result = ExecuteTestcaseController.execute_testcase(request.get_json())
        return make_response(CodeUtil.SUCCESS, data=result)
