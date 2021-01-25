# microservice
import os
import time
import sys

from flask import Flask, jsonify, request, abort

import definitions
import get_env


import cloudcoverage

app = Flask(__name__)



# see https://flask.palletsprojects.com/en/master/errorhandling/
# This is a custom exception
class InvalidAPIUsage(Exception):
    status_code = 400       # Need to read up & see if this is best practice
#
    def __init__(self, message, status_code=None, payload=None):
        super(InvalidAPIUsage, self).__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
            self.payload = payload
#
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message      # was rv['message']
        return rv


# common to all microservices
@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    answer = {}
    answer['error'] = e.message.__str__()
    response = jsonify(answer)
    response.status_code = 400

    return response


@app.errorhandler(404)
def page_not_found(error):
    answer = {}
    answer['error'] = error.__str__()

    response = jsonify(answer)
    response.status_code = 404

    return response


@app.errorhandler(500)
def server_error(error):
    answer = {}
    answer['error'] = error.__str__()

    response = jsonify(answer)
    response.status_code = 500

    return response


# -----------------------------------------------------


# an endpoint that can be polled with little overhead
@app.route('/status')
def status():
    answer = {}
    app_name = request.args.get('app_name')

    answer['service_name'] = 'coverage-service'
    answer['version'] = get_env.get_version()

    print('status() : app_name=' + app_name.__str__() + ', version=' + answer['version'])
    response = jsonify(answer)

    return response

@app.route('/abort_test')
def abort_request():
    answer = {}
    app_name = request.args.get('app_name')

    answer['api_calls'] = -1    # not yet implemented

    print('abort_test() : app_name=' + app_name.__str__())
    abort(500)


@app.route('/stats')
def stats():
    answer = {}
    app_name = request.args.get('app_name')

    answer['api_calls'] = -1    # not yet implemented

    print('status() : app_name=' + app_name.__str__() + ', api_calls=' + answer['api_calls'])
    response = jsonify(answer)

    return response


@app.route('/get_coverage')
def get_coverage_api():
    """

    :param app_name: e.g. name of the calling app so it can be identified in logs
    :return:
    """
    answer = {}
    app_name = request.args.get('app_name')

    filename = request.args.get('filename', None)

    print('get_coverage_api() : app_name=' + app_name.__str__() + ', filename=' + filename)

    # check to see the image exists / is readable - this is not done in get_coverage()
    try:
        fp = open(filename, 'rb')
    except (OSError, IOError):
        raise InvalidAPIUsage('Missing file or directory : ' + filename.__str__())

    new_image, coverage_percent = cloudcoverage.get_coverage(filename, is_daytime=True)

    answer['coverage'] = coverage_percent

    response = jsonify(answer)

    return response


if __name__ == '__main__':
    os.environ['PYTHONUNBUFFERED'] = "1"            # does this help with log buffering ?
    version = get_env.get_version()                 # container version

    print('coverage-service started, version=' + version)

    app.run(host='0.0.0.0', port=definitions.coverage_service_listen_port.__str__())
