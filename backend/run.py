from backend.app import db, app, api
from backend.controller.test_suite_controller import TestSuiteService
from backend.models.test_project_model import TestProjectModel
from backend.models.test_suite_model import TestSuiteModel
from backend.controller.test_hello import IndexService
from backend.controller.test_project_controller import TestProjectService

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

    api.add_resource(IndexService, '/')
    api.add_resource(TestProjectService, '/api/project')
    api.add_resource(TestSuiteService, '/api/suite')

    app.run(debug=True)
