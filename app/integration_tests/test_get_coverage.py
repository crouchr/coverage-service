import integration_definitions
from integration_tests import call_rest_api


def test_get_coverage_local_file():
    """
    File is shipped with (i.e. in) the container
    Test /status
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'
    query['filename'] = '../test_images/image397.jpg'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/get_coverage', query)

    assert status_code == 200
    assert response_dict['coverage'] == 68


def test_get_coverage_data_file_jpg():
    """
    File is located in the /data mount (external USB drive)
    Test /status
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'
    query['filename'] = integration_definitions.MEDIA_DIR + 'test_images/test_image_1.jpg'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/get_coverage', query)

    assert status_code == 200
    assert response_dict['coverage'] == 68


def test_get_coverage_data_file_png():
    """
    File is located in the /data mount (external USB drive)
    Test /status
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'
    query['filename'] = integration_definitions.MEDIA_DIR + 'test_images/test_image_1.png'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/get_coverage', query)

    assert status_code == 200
    assert response_dict['coverage'] == 99


def test_get_coverage_noexist_file():
    """
    File does not exist
    Test /status
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'
    query['filename'] = 'file_not_exist.png'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/get_coverage', query)

    assert status_code == 400
    assert 'Missing file or directory' in response_dict['error']
