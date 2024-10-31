from flask_restful import Resource
from backend.app import app


class IndexService(Resource):

    def get(self):
        return {'hello': 'hushan'}


if __name__ == '__main__':
    app.run(debug=True)
