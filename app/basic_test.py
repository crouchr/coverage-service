# The parts of the coverageimage that are red signify cloud
import cloudcoverage

def main():

    image = '../test_images/image397.jpg'
    image = '../ermin_cloud_images/metminiwx_1.png'

    coverageimage, coverage_percentage = cloudcoverage.get_coverage(image, is_daytime=True)

    # display the processed version of the image
    coverageimage.show()
    print('coverage percent = ' + coverage_percentage.__str__())


# A basic test program to show usage
if __name__ == '__main__':
    main()


# good images
# /cirrus/image391.jpg  1 %
# /cirrus/image397.jpg  68 %
