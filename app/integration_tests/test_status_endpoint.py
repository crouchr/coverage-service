# non-specific boilerplate code
import integration_definitions
from integration_tests import call_rest_api


def test_status():
    """
    Test /status
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/status', query)

    if response_dict is None:
        return None

    assert status_code == 200
    assert 'version' in response_dict
