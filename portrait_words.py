import os
import optparse

from PIL import Image

def main():
    """Retrieves file entered, manipulates it and saves a copy with a new name"""
    # Parse options
    parser = optparse.OptionParser()
    parser.add_option(
        "-f",
        dest="filename",
        help="Picture to modify",
        metavar="FILE"
    )
    (opts, args) = parser.parse_args()

    # Give user feedback if they forget an option and exit
    mandatory_options = ['filename']
    for option in mandatory_options:
        if not opts.__dict__[option]:
            print "Mandatory option is missing\n"
            parser.print_help()
            exit(-1)

    full_filename =  opts.filename
    if full_filename != None:
        try:
            image_data = Image.open(full_filename)
            new_image_data = wordize(image_data)
            safe_save(full_filename, new_image_data)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'

def wordize(image_data):
    posterized = black_posterize(image_data)
    return image_data

def black_posterize(image, threshold):
    copy_image = Image.new(image.mode, image.size, (255, 0, 0))
    width, height = copy_image.size
    pixels = image.load()
    copy_pixels = copy_image.load()
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            average = (r + g + b) / 3
            if average < threshold:
                copy_pixels[i, j] = (average, average, average)
    return copy_image

def invert(img):
    width, height = img.size
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = (255 - r, 255 - g, 255 - b)
    return img

def init_test(img):
    from PIL import Image
    from portrait_words import black_posterize
    image = Image.open(img)
    ret = black_posterize(image, 150)
    ret.save('output.jpg', 'JPEG')

def safe_save(full_filename, new_image_data):
    """
    Saves image with new name
    Inputs:
        full_filename, filename to be saved including extention e.g, myfile.jpg
        new_image_data, PIL Image data to be saved
    """
    filename, extention = os.path.splitext(full_filename)
    new_image_data.save(filename + '_modified' + extention)

if __name__ == "__main__":
    main()
