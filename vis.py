# Package imports
import os
from PIL import Image
from pytagcloud import create_tag_image, make_tags

# Project imports
from portrait_words import color_to_transparent
from portrait_words import safe_save

# Constants stored elsewhere
from yahoo_passwords import YAHOO_PASSWORDS_SMALL
from billabong_passwords import BILLABONG_PASSWORDS_SMALL
from myspace_passwords import MYSPACE_PASSWORDS_SMALL

WHITE = (255,255,255)
BLACK = (0,0,0)
BLACK_SET = (BLACK,)

def main():
    transparent_word_cloud(
        'cloud_yahoo.png',
        YAHOO_PASSWORDS_SMALL,
        0,
        'Droid Sans'
    )

    transparent_word_cloud(
        'cloud_billabong.png',
        BILLABONG_PASSWORDS_SMALL,
        45,
        'Lobster'
    )

    transparent_word_cloud(
        'cloud_myspace.png',
        MYSPACE_PASSWORDS_SMALL,
        -30,
        'Tangerine'
    )
    im = transparent_combine(
        "cloud_yahoo_modified.png",
        "cloud_billabong_modified.png",
        "cloud_myspace_modified.png"
    )
    safe_save("output.png", im)

def transparent_word_cloud(name, password_count, rotation_degrees, fontname):
    '''
    Args:
        name - string that is the name to save png
        password_count - list of tuples of [('password', count)]
        rotation_degrees - number of degrees to rotate text
        fontname - one of the fonts available to pytagcloud
    '''
    threshold = 10
    tags = make_tags(password_count, maxsize=120, colors=BLACK_SET)
    create_tag_image(tags, name, size=(900, 600), fontname=fontname)
    words = Image.open(name)
    words = color_to_transparent(words.rotate(rotation_degrees), WHITE, threshold)
    safe_save(name, words)
    os.remove(name)

def transparent_combine(image1_str, image2_str, image3_str):
    '''
    Combines images 2 and 3 onto image 1 such that
    the greatest alpha layer is preserved
    Args:
        All three are strings that correspond to a png file
    '''
    BLACK = (0,0,0)
    width = 890
    height = 500
    size = (0,0,width,height)

    image1 = Image.open(image1_str).crop(size)
    img1pix = image1.load()
    image2 = Image.open(image2_str).crop(size)
    img2pix = image2.load()
    image3 = Image.open(image3_str).crop(size)
    img3pix = image3.load()
    for x in range(width):
        for y in range(height):
            alpha_loc = 3
            cur_pix_im1 = img1pix[x, y]
            cur_pix_im2 = img2pix[x, y]
            cur_pix_im3 = img3pix[x, y]

            alpha = max(
                cur_pix_im1[alpha_loc],
                cur_pix_im2[alpha_loc],
                cur_pix_im3[alpha_loc],
            )
            if alpha != 0:
                img1pix[x, y] = BLACK
    return image1

if __name__ == "__main__":
    main()
