from backend.app import db, app, api

from backend.models.test_report_model import TestReportModel

from backend.controller.test_hello import IndexService
from backend.controller.test_project_controller import TestProjectService
from backend.controller.test_suite_controller import TestSuiteService
from backend.controller.test_case_controller import TestCaseService
from backend.controller.execute_testcase_controller import ExecuteTestcaseService
from backend.controller.test_user_controller import TestUserService


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

    api.add_resource(IndexService, '/')
    api.add_resource(TestProjectService, '/api/project')
    api.add_resource(TestSuiteService, '/api/suite')
    api.add_resource(TestCaseService, '/api/case')
    api.add_resource(ExecuteTestcaseService, '/api/run/case')
    api.add_resource(TestUserService, '/api/user')

    app.run(debug=True, use_reloader=False)
