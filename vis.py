# Package imports
import os
from PIL import Image
from pytagcloud import create_tag_image, make_tags

# Project imports
from portrait_words import color_to_transparent
from portrait_words import safe_save
from portrait_words import combine_with_mask

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
        'Lobster'
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
        'Lobster'
    )
    im = transparent_combine(
        Image.open("cloud_billabong_modified.png").crop((0,0,890,500)),
        Image.open("cloud_myspace_modified.png").crop((0,0,890,500)),
        Image.open("cloud_yahoo_modified.png").crop((0,0,890,500)),
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

def transparent_combine(image1, image2, image3):
    '''
    '''
    img1pix = image1.load()
    img2pix = image2.load()
    img3pix = image3.load()
    img1width, img1height = image1.size
    img2width, img2height = image2.size
    img3width, img3height = image3.size
    for x in range(img1width):
        for y in range(img1height):
            r1, g1, b1, a1 = img1pix[x, y]
            r2, g2, b2, a2 = img2pix[x, y]
            r3, g3, b3, a3 = img3pix[x, y]
            #TODO make turnary
            a = max(a1,a2,a3)
            if a != 0:
                img1pix[x, y] = (0,0,0)
    return image1

if __name__ == "__main__":
    main()
