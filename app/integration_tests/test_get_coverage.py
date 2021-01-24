import integration_definitions
import call_rest_api


def test_get_coverage():
    """
    Test /status
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'
    query['filename'] = '../test_images/image397.jpg'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/get_coverage', query)

    assert status_code == 200
    assert response_dict['coverage'] == 68

