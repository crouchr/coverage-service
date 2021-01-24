# microservice
import os
import time
import sys

from flask import Flask, jsonify, request

import definitions
import get_env

import cloudcoverage

app = Flask(__name__)


# fixme : this does not give info about the actual exception
@app.errorhandler(500)
def error_handling(error):
    answer = {}
    answer['error'] = str(error)

    print('coverage-service : error : ' + error.__str__())
    response = jsonify(answer, 500)

    return response


# an endpoint that can be polled with little overhead
@app.route('/status')
def status():
    answer = {}
    app_name = request.args.get('app_name')

    answer['status'] = 'OK'
    answer['service_name'] = 'coverage-service'
    answer['version'] = get_env.get_version()

    print('status() : app_name=' + app_name.__str__() + ', version=' + answer['version'])
    response = jsonify(answer)

    return response


@app.route('/stats')
def stats():
    answer = {}
    app_name = request.args.get('app_name')

    answer['status'] = 'OK'
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
    try:
        answer = {}
        app_name = request.args.get('app_name')

        filename = request.args.get('filename', None)

        print('get_coverage_api() : app_name=' + app_name.__str__() + ', filename=' + filename)

        new_image, coverage_percent = cloudcoverage.get_coverage(filename, is_daytime=True)

        answer['status'] = 'OK'
        answer['coverage'] = coverage_percent

        response = jsonify(answer)

        return response

    except Exception as e:
        answer['function'] = 'get_coverage_api()'
        answer['error'] = str(e)
        print('get_coverage_api() : app_name=' + app_name.__str__() + ', error : ' + e.__str__())
        response = jsonify(answer, 500)

        return response


if __name__ == '__main__':
    os.environ['PYTHONUNBUFFERED'] = "1"            # does this help with log buffering ?
    version = get_env.get_version()                 # container version

    print('coverage-service started, version=' + version)

    app.run(host='0.0.0.0', port=definitions.coverage_service_listen_port.__str__())
