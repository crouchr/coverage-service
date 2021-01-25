# non-specific boilerplate code

import integration_definitions
from integration_tests import call_rest_api


def test_missing_url():
    """
    Test response to missing URL
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/get_no_exist_url', query)

    assert status_code == 404


def test_http_500():
    """
    Test response to http 500
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/abort_test', query)

    assert status_code == 500
