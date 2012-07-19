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
            print 'Beginning portrait word transform...'
            image_data = Image.open(full_filename)
            new_image_data = wordize(image_data)
            name = safe_save(full_filename, new_image_data)
            print 'Portrait word transform saved to {0}'.format(name)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'

def wordize(image_data):
    posterized = black_posterize(image_data, 150)
    transparent = color_to_transparent(posterized, (255, 0, 0), 10)
    #text_img = Image.open('cloud_billabong_modified.png')
    text_img = Image.open('debug_text.png')
    text_x, text_y = text_img.size
    output_img = combine_with_mask(transparent, text_img, transparent)
    transparent_to_color(output_img, (255, 255, 255))
    return output_img

def combine_with_mask(image1, image2, mask):
    '''
    Combines two images into one image such that image2 exists on top of image
    1. The alpha of the mask is used to determine where image2 is pasted onto
    image1.
    WARNING AT THIS POINT IN DEVELOPMENT THIS
    CODE DOES NOT DO BOUNDS CHECKING
    '''
    image1_copy = image1.copy()
    image2 = image2.convert('RGBA')
    img1pix = image1.load()
    img2pix = image2.load()
    maskpix = mask.load()
    img1width, img1height = image1.size
    img2width, img2height = image2.size
    for x in range(img1width):
        for y in range(img1height):
            r, g, b, a = maskpix[x, y]
            if a != 0:
                r, g, b, a = img1pix[x, y]
                grayscale_magnitude = (r + g + b) / 3
                r2, g2, b2, a2 = img2pix[x % img2width, y % img2height] #TODO BOUNDS CHECKING
                if (r2, g2, b2) != (255, 255, 255):
                    img1pix[x, y] = (int(r2 * (grayscale_magnitude / float(255))), int(g2 * (grayscale_magnitude / float(255))), int(b2 * (grayscale_magnitude / float(255))), a2)
                else:
                    img1pix[x, y] = (255, 255, 255, 0)
    grayscale_modify(image1, image1_copy)
    return image1

def grayscale_modify(sink, source):
    '''
    Uses the source image to modify the darkness of the sink image.
    This method will FAIL if the size of the sink and the source are
    not the same
    '''
    if (sink.size != source.size):
        #TODO FAIL GRACEFULLY
        return
    width, height = sink.size
    sink_pixels = sink.load()
    source_pixels = source.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = sink_pixels[x, y]
            r2, g2, b2, a2 = source_pixels[x, y]
            if a == 255:
                source_pixels[x, y] = (r, g, b, a)

def transparent_to_color(img, color):
    '''
    Converts all pixels with alpha = 0 to a color. Color is a 3-tuple of 
    RGB values.
    '''
    img_pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img_pixels[x, y]
            if (a == 0):
                img_pixels[x, y] = (color[0], color[1], color[2], 255)
    

def black_posterize(image, threshold):
    '''
    Posterizes an image such that light pixels are rendered transparent.
    Returns a new image.
    @author Sean Gillespie
    '''
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

# Inverts an image. This operation is done in place and does not return
# a new image.
# @author Sean Gillespie
def invert(img):
    width, height = img.size
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = (255 - r, 255 - g, 255 - b)

# Given the input image, this method changes all pixels with the exact color
# in the parameters to be transparent. The threshold is required because
# exact colors don't always happen, which is bizarre...
# @author Sean Gillespie
def color_to_transparent(img, color, threshold):
    converted_img = img.convert('RGBA') # allow manipulation of alpha
    pixels = converted_img.load()
    width, height = converted_img.size
    for x in range(width):
        for y in range(height):
            diff = (pixels[x, y][0] - color[0], pixels[x, y][1] - color[1], pixels[x, y][2] - color[2])
            if abs(diff[0]) < threshold and abs(diff[1]) < threshold and abs(diff[2]) < threshold:
                pixels[x, y] = (pixels[x, y][0], pixels[x, y][1], pixels[x, y][2], 0)
    return converted_img

# for debug purposes only
# @author Sean Gillespie
def init_test(img):
    from PIL import Image
    from portrait_words import black_posterize
    image = Image.open(img)
    ret = black_posterize(image, 150)
    ret2 = color_to_transparent(ret, (255, 0, 0), 10)
    ret2.save('output.png', 'png')

def safe_save(full_filename, new_image_data):
    """
    Saves image with new name
    Inputs:
        full_filename, filename to be saved including extention e.g, myfile.jpg
        new_image_data, PIL Image data to be saved
    Returns
        The name of the file after being saved
    """
    filename, extention = os.path.splitext(full_filename)
    new_filename = filename + '_modified' + extention
    new_image_data.save(new_filename)
    return new_filename
    

if __name__ == "__main__":
    main()
