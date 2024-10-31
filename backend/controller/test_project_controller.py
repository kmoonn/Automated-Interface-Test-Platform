from flask import request

from backend.app import app, db, api
from flask_restful import Resource

from backend.models.test_project_model import TestProjectModel


class TestProjectController(Resource):
    def __init__(self):
        pass

    @classmethod
    def add_project(cls, project_data):
        data = TestProjectModel(**project_data)
        db.session.add(data)
        db.session.commit()
        db.session.close()


class TestProjectService(Resource):
    def get(self):
        pass

    def post(self):
        try:
            project_data = request.json
            TestProjectController.add_project(project_data)
            return {'status': '1', 'message': '添加测试计划成功', 'data': project_data}, 200
        except Exception as e:
            app.logger.info(e)
            return {'status': '-1', 'message': '添加测试计划失败'}, 500

    def put(self):
        pass

    def delete(self):
        pass
