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

if __name__ == "__main__":
    main()
