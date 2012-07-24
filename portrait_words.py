import os
import optparse
import math

from PIL import Image

def main():
    """
    Retrieves file entered, manipulates it and saves a copy with a new name
    """
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
            name = safe_save(full_filename, new_image_data, force_png=True)
            print 'Portrait word transform saved to {0}'.format(name)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'

def wordize(image_data):
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    posterized = black_posterize(image_data, 150)
    transparent = color_to_transparent(posterized, RED, 10)
    text_img = Image.open('output_modified.png')
    output_img = combine_with_mask(transparent, text_img, transparent)
###    transparent_to_color(output_img, WHITE)
    gradient_fill(
        gradient_func_factory(
            (255, 215, 0),
            (178, 34, 34),
            output_img.size
        ),
        output_img
    )
    return output_img

def combine_with_mask(image1, image2, mask):
    '''
    Combines two images into one image such that image2 exists on top of image1
    1. The alpha of the mask is used to determine where image2 is pasted onto
    image1.
    WARNING AT THIS POINT IN DEVELOPMENT THIS
    CODE DOES NOT DO BOUNDS CHECKING
    '''
    image1_copy = image1.copy()
    image2 = image2.convert('RGBA')
    wid, hig = image2.size
    image2 = image2.crop((wid/10,hig/10,wid,hig))
    img1pix = image1.load()
    img2pix = image2.load()
    maskpix = mask.load()
    img1width, img1height = image1.size
    img2width, img2height = image2.size
    for x in range(img1width):
        for y in range(img1height):
            # get the alpha layer
            alpha = maskpix[x, y][3]
            if alpha != 0:
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
            alpha = img_pixels[x, y][3]
            if (alpha == 0):
                img_pixels[x, y] = (color[0], color[1], color[2], 255)

def black_posterize(image, threshold):
    '''
    Posterizes an image such that light pixels are rendered red.
    Returns a new image.
    '''
    copy_image = Image.new(image.mode, image.size, (255, 0, 0))
    width, height = copy_image.size
    pixels = image.load()
    copy_pixels = copy_image.load()
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            new_color = split_black_gray(r, g, b)
            if new_color != (r, g, b):
                copy_pixels[i, j] = new_color
    return copy_image

def split_black_gray(red_val, green_val, blue_val):
    '''
    Takes red green and blue values and splits them
    into either black, gray or origional
    returns a tuple of the form (red, green, blue)
    '''
    gray_lower_threshold = 50
    gray_upper_threshold = 160
    black_threshold = 100
    if ((red_val > gray_lower_threshold and red_val < gray_upper_threshold) and
          (green_val > gray_lower_threshold and green_val < gray_upper_threshold) and
          (blue_val > gray_lower_threshold and blue_val < gray_upper_threshold)):
        color = (127,127,127) # gray
    elif (red_val < black_threshold and
          green_val < black_threshold and
          blue_val < black_threshold):
        color = (0, 0, 0) # black
    else:
        color = (red_val, green_val, blue_val)
    return color

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
            diff = (
                pixels[x, y][0] - color[0],
                pixels[x, y][1] - color[1],
                pixels[x, y][2] - color[2]
            )
            if (abs(diff[0]) < threshold and
                abs(diff[1]) < threshold and
                abs(diff[2]) < threshold):
                pixels[x, y] = (
                    pixels[x, y][0],
                    pixels[x, y][1],
                    pixels[x, y][2],
                    0
                )
    return converted_img

def gradient_fill(function, img, replace_color=(0, 0, 0), tolerance=10):
    '''
    Gradient takes in a function and an image and applies that function
    to every pixel. The function MUST take in an X coordinate and Y coordinate
    as parameters (i.e. func(x, y)). The image can be any image in any mode.

    The replace_color parameter defines a color that the gradient will be
    replacing in the image. The tolerance parameter is the distance away
    from the replace_color that the program will replace with the gradient.
 
    Inputs:
       function, the "gradient" function to be applied at every pixel
       img, the PIL Image to use
       replace_color, the color to replace with the gradient
       tolerance, the range of colors near the replace_color that will
                  be allowed to count as the replace_color
    
    Returns:
       Nothing
    '''
    width, height = img.size
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            img_r, img_g, img_b, img_a = pixels[x, y]
            replace_r, replace_g, replace_b = replace_color
            if (abs(img_r - replace_r) < tolerance and
                abs(img_g - replace_g) < tolerance and
                abs(img_b - replace_b) < tolerance):
                pixels[x, y] = function(x, y)

def gradient_func_factory(color1, color2, img_size):
    '''
    This function generates a gradient function for use with gradient_fill.
    Inputs:
       Color1, the 'first' color, and the color that will be used at the top
               left of the image. Color1 will fade into color2.
       Color2, the 'second' color, and the color that will be used at the bottom
               right of the image. Color2 is faded into by color1.
       img_size, the size of an image in the form of a tuple (width, height)
    Returns:
       A function that, given X and Y coordinates, will return the appropriate
       color pixel such that the entire image becomes a gradient.
    '''
    magnitude = lambda x, y: math.sqrt(x**2 + y**2)
    return lambda x, y: color_weighted_avg(
        color1,
        1 - (magnitude(x, y) / magnitude(img_size[0], img_size[1])),
        color2,
        magnitude(x, y) / magnitude(img_size[0], img_size[1])
    )
    
def color_scalar_multiply(color, scale_factor):
    '''
    Takes all elements of a color tuple and multiplies it by a scale factor.
    '''
    color_out = ()
    for element in color:
        color_out = color_out + eval('({0},)'.format(str(int(element * scale_factor))))
    return color_out

def color_linear_add(color1, color2):
    if len(color1) != len(color2):
        return None
    color_out = ()
    for i in range(len(color1)):
        color_out = color_out + eval('({0},)'.format(str(color1[i] + color2[i])))
    return color_out

def color_weighted_avg(color1, weight1, color2, weight2):
    '''
    Calculates a weighted average between two colors using the given
    colors and weights.
    '''
    return color_linear_add(color_scalar_multiply(color1, weight1),
                            color_scalar_multiply(color2, weight2))
    

def safe_save(full_filename, new_image_data, force_png=False):
    """
    Saves image with new name
    Inputs:
        full_filename, filename to be saved including extention e.g, myfile.jpg
        new_image_data, PIL Image data to be saved
    Returns
        The name of the file after being saved
    """
    filename, extention = os.path.splitext(full_filename)
    if force_png:
        extention = '.png'
    new_filename = filename + '_modified' + extention
    new_image_data.save(new_filename)
    return new_filename
    

if __name__ == "__main__":
    main()
