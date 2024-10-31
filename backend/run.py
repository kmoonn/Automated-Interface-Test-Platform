from backend.app import db, app, api
from backend.controller.test_hello import IndexService
from backend.controller.test_project_controller import TestProjectService

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

    api.add_resource(IndexService, '/')
    api.add_resource(TestProjectService, '/api/project')

    app.run(debug=True)
