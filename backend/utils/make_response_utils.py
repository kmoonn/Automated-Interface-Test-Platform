import json

from backend.utils.code_utils import CodeUtil
from flask import Response


def make_response(status=CodeUtil.SUCCESS, data=None, **kwargs):
    response = {
            'status': status,
            'msg': CodeUtil.MSG[status],
            'data': data
        }
    if kwargs:
        for key, value in kwargs.items():
            response[key] = value
    return Response(json.dumps(response), mimetype='application/json')


def make_exception_response(status=CodeUtil.ERROR, msg=None, data=None):
    return Response(json.dumps(
        {
            'status': str(status),
            'msg': msg if msg else CodeUtil.MSG[str(status)],
            'data': data
        }
    ), mimetype='application/json')
