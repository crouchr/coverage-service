import cloudcoverage


def test_get_coverage():
    """
    :return:
    """
    image = '../../test_images/image397.jpg'

    coverageimage, coverage_percentage = cloudcoverage.get_coverage(image, is_daytime=True)

    assert coverage_percentage == 68

