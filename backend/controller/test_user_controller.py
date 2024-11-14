from flask_restful import Resource


class TestUserController(Resource):
    def __init__(self):
        pass

    @classmethod
    def add_user(cls,username,password):
        pass

    @classmethod
    def delete_user(cls,username):
        pass

    @classmethod
    def modify_user(cls,username,password):
        pass

    @classmethod
    def query_user_by_id(cls,user_id):
        pass

    @classmethod
    def query_user_by_name(cls,username):
        pass

    @classmethod
    def query_list(cls, page, size):
        pass


class TestUserService(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass