import datetime

from flask import request
from flask_restful import Resource

from backend.app import db, app
from backend.models.test_project_model import TestProjectModel
from backend.models.test_suite_model import TestSuiteModel
from backend.utils.code_utils import CodeUtil
from backend.utils.exception_utils import REQ_IS_EMPTY_ERROR, REQ_TYPE_ERROR, REQ_KEY_ERROR, REQ_VALUE_ERROR
from backend.utils.make_response_utils import make_response


class TestSuiteController(Resource):
    def __init__(self):
        pass

    @classmethod
    def add_suite(cls, suite_data):
        project_id = suite_data['project_id']
        project_data = TestProjectModel.query.filter_by(id=project_id, isDeleted=0).first()
        if project_data is None:
            return None
        data = TestSuiteModel(**suite_data)
        db.session.add(data)
        db.session.commit()
        db.session.close()
        return True

    @classmethod
    # 查询测试套件详情
    def query_suite_by_id(cls, id):
        suite_detail_data = TestSuiteModel.query.filter_by(id=id, isDeleted=False).first()
        if suite_detail_data is None:
            return []
        suite_detail_data = suite_detail_data.to_dict()
        suite_detail_data.update({"created_at": str(suite_detail_data.get("created_at"))})
        if suite_detail_data.get("updated_at"):
            suite_detail_data.update({"updated_at": str(suite_detail_data.get("updated_at"))})
        return suite_detail_data

    @classmethod
    # 根据测试套件的名称，搜索测试计划
    def query_suite_by_name(cls, suite_name):
        suite_search_data = TestSuiteModel.query.filter(
            TestSuiteModel.suite_name.like(f'%{suite_name}%'),
            TestSuiteModel.isDeleted == 0).all()

        response_list = []
        for suite_data in suite_search_data:
            suite_dictdata = suite_data.to_dict()  # 把model中的数据转化成dict
            suite_dictdata.update({"created_at": str(suite_dictdata.get("created_at"))})  # 修改创建时间对象为字符串对象
            if suite_dictdata.get("updated_at"):
                suite_dictdata.update({"updated_at": str(suite_dictdata.get("updated_at"))})
            response_list.append(suite_dictdata)
        return response_list

    @classmethod
    # 查询测试套件列表
    def query_list(cls, page=1, size=10):
        all_data = TestSuiteModel.query \
            .filter(TestSuiteModel.isDeleted == 0) \
            .slice((page - 1) * size, page * size) \
            .all()

        response_list = []
        for suite_data in all_data:
            suite_dictdata = suite_data.to_dict()  # 把model中的数据转化成dict
            suite_dictdata.update({"created_at": str(suite_dictdata.get("created_at"))})  # 修改创建时间对象为字符串对象
            if suite_dictdata.get("updated_at"):
                suite_dictdata.update({"updated_at": str(suite_dictdata.get("updated_at"))})
            response_list.append(suite_dictdata)
        return response_list

    @classmethod
    def modify_suite(cls, suite_id, project_id, suite_name, description):
        project_data = TestProjectModel.query.filter_by(id=project_id, isDeleted=0).first()
        if project_data is None:
            app.logger.info(f"测试计划id为{project_id}的数据不存在")
            return False
        origin_data = TestSuiteModel.query.filter_by(id=suite_id, project_id=project_id, isDeleted=0).first()  # 根据id查询出之前的数据
        if origin_data is None:
            return False
        origin_suite_name = origin_data.suite_name  # 读取数据库中的测试套件名称
        origin_description = origin_data.description  # 读取数据库中的测试套件的备注
        modify_data = {
            "suite_name": suite_name if suite_name else origin_suite_name,
            "description": description if description else origin_description
        }

        if suite_name or description:  # 外部传入的project_name和description至少要有一个不为空才能触发修改，才能有时间的修改
            update_time = str(datetime.datetime.now())
            modify_data.update({"updated_at": update_time})
        TestSuiteModel.query.filter_by(id=suite_id, isDeleted=0).update(modify_data)
        db.session.commit()
        db.session.close()

        return modify_data

    @classmethod
    # 根据id查询要删除的数据
    def delete_suite(cls, suite_id, project_id):
        project_data = TestProjectModel.query.filter_by(id=project_id, isDeleted=0).first()
        if project_data is None:
            return False
        origin_data = TestSuiteModel.query.filter_by(id=suite_id, project_id=project_id, isDeleted=0).first()
        if origin_data is None:
            return False
        TestSuiteModel.query.filter_by(id=suite_id, isDeleted=0).update({"isDeleted": 1})
        db.session.commit()
        db.session.close()
        return True


class TestSuiteService(Resource):
    def get(self):
        if not request.args:
            raise REQ_IS_EMPTY_ERROR()
        if not request.args.get("type"):
            raise REQ_KEY_ERROR()

        action_type = request.args.get("type")

        if action_type == "query_detail":
            if not request.args.get("id"):
                raise REQ_KEY_ERROR()
            response_data = TestSuiteController.query_suite_by_id(request.args.get("id"))
            if len(response_data) < 1:
                return make_response(status=CodeUtil.SUCCESS, data=response_data)
            return make_response(status=CodeUtil.SUCCESS, data=response_data)

        if action_type == "search":
            if not request.args.get("suite_name"):
                raise REQ_KEY_ERROR()
            response_data = TestSuiteController.query_suite_by_name(request.args.get("suite_name"))

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
            response_data = TestSuiteController.query_list(page, size)
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
        project_id = request.get_json().get("project_id")
        suite_name = request.get_json().get("suite_name")
        if not project_id or not suite_name:
            raise REQ_KEY_ERROR()
        if not isinstance(project_id, int) or not isinstance(suite_name, str):
            raise REQ_VALUE_ERROR()

        suite_data = request.json
        if TestSuiteController.add_suite(suite_data):
            return make_response(
                status=CodeUtil.SUCCESS,
                data=suite_data
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

        suite_id = request.get_json().get("id")
        project_id = request.get_json().get("project_id")
        suite_name = request.get_json().get("suite_name")
        description = request.get_json().get("description")

        response_data = TestSuiteController.modify_suite(suite_id, project_id, suite_name, description)
        if response_data:
            return make_response(status=CodeUtil.SUCCESS, data=response_data)
        else:
            return make_response(status=CodeUtil.FAIL)

    def delete(self):
        if not request.data:
            raise REQ_IS_EMPTY_ERROR()
        if not request.is_json:
            raise REQ_TYPE_ERROR()
        if not request.get_json().get("id") or not request.get_json().get("project_id"):
            raise REQ_KEY_ERROR()

        suite_id = request.get_json().get("id")
        project_id = request.get_json().get("project_id")
        if TestSuiteController.delete_suite(suite_id, project_id):
            return make_response(status=CodeUtil.SUCCESS, data=None)
        else:
            return make_response(status=CodeUtil.FAIL)
