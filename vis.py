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
        0,
        'Tangerine'
    )
    im = transparent_combine(
        Image.open("cloud_billabong_modified.png").crop((0,0,890,500)),
        Image.open("cloud_myspace_modified.png").crop((0,0,890,500)),
        Image.open("cloud_yahoo_modified.png").crop((0,0,890,500)),
    )
    im.rotate(Image.ROTATE_90)
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

def transparent_combine(image1, image2, image3):
    '''
    Combines 3 images such that the greatest alpha layer is preserved
    Args:
        All three PIL image data of the same size
    '''
    BLACK = (0,0,0)
    img1pix = image1.load()
    img2pix = image2.load()
    img3pix = image3.load()
    img1width, img1height = image1.size
    for x in range(img1width):
        for y in range(img1height):
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
