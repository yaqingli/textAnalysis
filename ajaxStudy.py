from bottle import route, run, debug, template, request
import json


@route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.params.get('a', 0, type=int)
    b = request.params.get('b', 0, type=int)
    return json.dumps({'result': a+b})


@route('/')
def index():
    return template('ajaxStudy.tpl', request=request)


debug(True)
run(port=9030)