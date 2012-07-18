# Package imports
import os
from PIL import Image
from pytagcloud import create_tag_image, make_tags

# Project imports
from portrait_words import color_to_transparent
from portrait_words import safe_save

# Constants stored elsewhere
from yahoo_passwords import YAHOO_PASSWORDS_SMALL
from billabong_paswords import BILLABONG_PASWORDS_SMALL
from myspace_passwords import MYSPACE_PASSWORDS_SMALL

WHITE = (255,255,255)
BLACK = (0,0,0)
BLACK_SET = (BLACK,)

yahoo_tags = make_tags(YAHOO_PASSWORDS_SMALL, maxsize=120, colors=BLACK_SET)
billabong_tags = make_tags(BILLABONG_PASWORDS_SMALL, maxsize=120, colors=BLACK_SET)
myspace_tags = make_tags(MYSPACE_PASSWORDS_SMALL, maxsize=120, colors=BLACK_SET)

create_tag_image(yahoo_tags, 'cloud_yahoo.png', size=(900, 600), fontname='Lobster')
create_tag_image(billabong_tags, 'cloud_billabong.png', size=(900, 600), fontname='Lobster')
create_tag_image(myspace_tags, 'cloud_myspace.png', size=(900, 600), fontname='Lobster')

def transparent_word_cloud(name, password_count, fontname, rotation_degrees):
    '''
    Args:
        name - string that is the name to save png
        password_count - list of tuples of [('password', count)]
        fontname - one of the fonts available to pytagcloud
        rotation_degrees - number of degrees to rotate text
    '''
    threshold = 10
    yahoo_tags = make_tags(password_count, maxsize=120, colors=BLACK)
    create_tag_image(yahoo_tags, name, size=(900, 600), fontname=fontname)
    words = Image.open(name)
    words = color_to_transparent(yahoo_words.rotate(rotation_degrees), WHITE, threshold)
    safe_save(name, words)
    os.remove(name)
