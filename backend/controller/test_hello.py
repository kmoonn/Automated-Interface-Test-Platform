from flask_restful import Resource


class IndexService(Resource):

    def get(self):
        return {'hello': 'hushan'}

