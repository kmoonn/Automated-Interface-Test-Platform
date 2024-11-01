from datetime import datetime

from flask import request
from flask_restful import Resource

from backend.app import db, app
from backend.models.test_case_model import TestCaseModel
from backend.models.test_suite_model import TestSuiteModel
from backend.utils.code_utils import CodeUtil
from backend.utils.exception_utils import REQ_IS_EMPTY_ERROR, REQ_TYPE_ERROR, REQ_KEY_ERROR, REQ_VALUE_ERROR
from backend.utils.make_response_utils import make_response


class TestCaseController(Resource):
    
    def __init__(self):
        pass
    
    @classmethod
    def add_case(cls, case_data):
        suite_id = case_data['suite_id']
        suite_data = TestSuiteModel.query.filter_by(id=suite_id, isDeleted=0).first()
        if suite_data is None:
            app.logger.info(f"测试计划id为{suite_id}的数据不存在")
            return None
        data = TestCaseModel(**case_data)
        db.session.add(data)
        db.session.commit()
        db.session.close()
        return True

    @classmethod
    # 查询测试用例详情
    def query_case_by_id(cls, id):
        case_detail_data = TestCaseModel.query.filter_by(id=id, isDeleted=False).first()
        app.logger.info(f"查询的测试用例id为：{id} 的详情数据为：{case_detail_data}")
        if case_detail_data is None:
            return []
        app.logger.info(f"查询的测试用例id为：{id} 的详情数据转化为json后：{case_detail_data.to_dict()}")
        case_detail_data = case_detail_data.to_dict()
        case_detail_data.update({"created_at": str(case_detail_data.get("created_at"))})
        if case_detail_data.get("updated_at"):
            case_detail_data.update({"updated_at": str(case_detail_data.get("updated_at"))})
        app.logger.info(f"把日期对象转化为字符串之后，的结果为：{case_detail_data}")
        return case_detail_data

    @classmethod
    # 根据测试用例的名称，搜索测试计划
    def query_case_by_name(cls, case_name):
        project_search_data = TestCaseModel.query.filter(
            TestCaseModel.project_name.like(f'%{case_name}%'),
            TestCaseModel.isDeleted == 0).all()
        app.logger.info(f"根据测试用例名称 [{case_name}] 搜索出来的数据有：{project_search_data}")

        response_list = []
        for case_data in project_search_data:
            case_dictdata = case_data.to_dict()  # 把model中的数据转化成dict
            case_dictdata.update({"created_at": str(case_dictdata.get("created_at"))})  # 修改创建时间对象为字符串对象
            if case_dictdata.get("updated_at"):
                case_dictdata.update({"updated_at": str(case_dictdata.get("updated_at"))})
            response_list.append(case_dictdata)
        app.logger.info(f"根据测试用例名称 [{case_name}] 搜索出来的数据并转化为json后：{response_list}")
        return response_list

    @classmethod
    # 查询测试用例列表
    def query_list(cls, page=1, size=10):
        all_data = TestCaseModel.query \
            .filter(TestCaseModel.isDeleted == 0) \
            .slice((page - 1) * size, page * size) \
            .all()
        app.logger.info(f"查询出的测试用例列表数据为：{all_data}")

        response_list = []
        for case_data in all_data:
            case_dictdata = case_data.to_dict()  # 把model中的数据转化成dict
            case_dictdata.update({"created_at": str(case_dictdata.get("created_at"))})  # 修改创建时间对象为字符串对象
            if case_dictdata.get("updated_at"):
                case_dictdata.update({"updated_at": str(case_dictdata.get("updated_at"))})
            response_list.append(case_dictdata)
        app.logger.info(f"查询出的测试用例列表数据并转化为json为：{all_data}")
        return response_list

    @classmethod
    def modify_case(cls, id, suite_id, case_name, description):
        suite_data = TestSuiteModel.query.filter_by(id=suite_id, isDeleted=0).first()
        if suite_data is None:
            app.logger.info(f"测试计划id为{suite_id}的数据不存在")
            return None
        origin_data = TestCaseModel.query.filter_by(id=id, suite_id=suite_id, isDeleted=0).first()  # 根据id查询出之前的数据
        if not origin_data:
            return None
        origin_case_name = origin_data.case_name  # 读取数据库中的测试用例名称
        origin_description = origin_data.description  # 读取数据库中的测试用例的备注
        modify_data = {
            "project_name": case_name if case_name else origin_case_name,
            "description": description if description else origin_description
        }

        if case_name or description:  # 外部传入的project_name和description至少要有一个不为空才能触发修改，才能有时间的修改
            update_time = str(datetime.now())
            modify_data.update({"updated_at": update_time})
        TestCaseModel.query.filter_by(id=id, isDeleted=0).update(modify_data)
        db.session.commit()
        db.session.close()

        return modify_data

    @classmethod
    # 根据id查询要删除的数据
    def delete_case(cls, id, suite_id):
        suite_data = TestSuiteModel.query.filter_by(id=suite_id, isDeleted=0).first()
        if suite_data is None:
            return None
        origin_data = TestCaseModel.query.filter_by(id=id, suite_id=suite_id, isDeleted=0).first()
        if not origin_data:
            return None
        TestCaseModel.query.filter_by(id=id, isDeleted=0).update({"isDeleted": 1})
        db.session.commit()
        db.session.close()


class TestCaseService(Resource):

    def get(self):
        if not request.args:
            raise REQ_IS_EMPTY_ERROR()
        if not request.args.get("type"):
            raise REQ_KEY_ERROR()

        action_type = request.args.get("type")

        if action_type == "query_detail":
            if not request.args.get("id"):
                raise REQ_KEY_ERROR()
            response_data = TestCaseController.query_case_by_id(request.args.get("id"))
            if len(response_data) < 1:
                return make_response(status=CodeUtil.SUCCESS, data=response_data)
            return make_response(status=CodeUtil.SUCCESS, data=response_data)

        if action_type == "search":
            if not request.args.get("case_name"):
                raise REQ_KEY_ERROR()
            response_data = TestCaseController.query_case_by_name(request.args.get("case_name"))

            return make_response(status=CodeUtil.SUCCESS, data=response_data)

        if action_type == "query_list":
            page = request.args.get("page")
            if page:
                if page.isdigit():
                    page = int(page)
                else:
                    return make_response(status=CodeUtil.SUCCESS, data=[])
            size = request.args.get("size")
            if size:
                if size.isdigit():
                    size = int(size)
                else:
                    return make_response(status=CodeUtil.SUCCESS, data=[])
            response_data = TestCaseController.query_list(page, size)
            total_count = len(response_data)
            return make_response(status=CodeUtil.SUCCESS,
                                 data=response_data,
                                 total_count=total_count,
                                 page=page,
                                 size=size)
        return make_response(status=CodeUtil.SUCCESS)

    def post(self):
        if not request.data:
            raise REQ_IS_EMPTY_ERROR()
        if not request.is_json:
            raise REQ_TYPE_ERROR()
        suite_id = request.get_json().get("suite_id")
        case_name = request.get_json().get("case_name")
        if not case_name or not suite_id:
            raise REQ_KEY_ERROR()
        if not isinstance(suite_id, int) or not isinstance(case_name, str):
            raise REQ_VALUE_ERROR()

        case_data = request.json
        if TestCaseController.add_case(case_data):
            return make_response(
                status=CodeUtil.SUCCESS,
                data=case_data
            )
        else:
            return make_response(status=CodeUtil.FAIL)

    def put(self):
        if not request.data:
            raise REQ_IS_EMPTY_ERROR()
        if not request.is_json:
            raise REQ_TYPE_ERROR()
        if not request.get_json().get("id"):
            raise REQ_KEY_ERROR()

        id = request.get_json().get("id")
        suite_id = request.get_json().get("suite_id")
        case_name = request.get_json().get("case_name")
        description = request.get_json().get("description")

        response_data = TestCaseController.modify_case(id, suite_id, case_name, description)
        if response_data:
            return make_response(status=CodeUtil.SUCCESS, data=response_data)
        else:
            return make_response(status=CodeUtil.FAIL)

    def delete(self):
        if not request.data:
            raise REQ_IS_EMPTY_ERROR()
        if not request.is_json:
            raise REQ_TYPE_ERROR()
        if not request.get_json().get("id") or not request.get_json().get("suite_id"):
            raise REQ_KEY_ERROR()

        id = request.get_json().get("id")
        suite_id = request.get_json().get("suite_id")
        if TestCaseController.delete_case(id,suite_id):
            return make_response(status=CodeUtil.SUCCESS, data=None)
        else:
            return make_response(status=CodeUtil.FAIL)