# Package imports
import os
from PIL import Image
from pytagcloud import create_tag_image, make_tags

# Project imports
from portrait_words import color_to_transparent
from portrait_words import safe_save

# Constants stored elsewhere
from british_words import BRITISH_WORDS_SMALL

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK_SET = (BLACK,)

def main():
    '''
    Creates word clouds of the leaked passwords
    from yahoo, myspace, and billabong.
    Word cloud is either black or transparent.
    Output file is a png
    '''
    cloud_width = 1800
    cloud_height = 1200
    image1 = transparent_word_cloud(
        'cloud_yahoo.png',
        BRITISH_WORDS_SMALL,
        0,
        'Droid Sans',
        cloud_width,
        cloud_height
    )

    image2 = transparent_word_cloud(
        'cloud_billabong.png',
        BRITISH_WORDS_SMALL,
        90,
        'Philosopher',
        cloud_width,
        cloud_height
    )

    image3 = transparent_word_cloud(
        'cloud_myspace.png',
        BRITISH_WORDS_SMALL,
        180,
        'Tangerine',
        cloud_width,
        cloud_height
    )
    transparent_combination = transparent_combine(cloud_width, cloud_height, image1, image2, image3)
    safe_save("output.png", transparent_combination)

def transparent_word_cloud(name, password_count, rotation_degrees, fontname, width, height):
    '''
    Args:
        name - string that is the name to save png
        password_count - list of tuples of [('password', count)]
        rotation_degrees - number of degrees to rotate text
        fontname - one of the fonts available to pytagcloud
    '''
    threshold = 10
    tags = make_tags(password_count, maxsize=120, colors=BLACK_SET)
    create_tag_image(tags, name, size=(width, height), fontname=fontname)
    words = Image.open(name)
    words = color_to_transparent(
        words.rotate(rotation_degrees),
        WHITE,
        threshold
    )
    os.remove(name)
    return words

def transparent_combine(img_width, img_height, image1, image2, image3):
    '''
    Combines images 2 and 3 onto image 1 such that
    the greatest alpha layer is preserved
    Args:
        All three are PIL image data
    '''
    # This is a hack to make the words more dense
    width = int(img_width * .9)
    height = int(img_height * .9)

    size = (0, 0, width, height)

    image1 = image1.crop(size)
    image2 = image2.crop(size)
    image3 = image3.crop(size)

    img1pix = image1.load()
    img2pix = image2.load()
    img3pix = image3.load()

    for row  in range(width):
        for col in range(height):
            alpha_loc = 3
            cur_pix_im1 = img1pix[row, col]
            cur_pix_im2 = img2pix[row, col]
            cur_pix_im3 = img3pix[row, col]

            alpha = max(
                cur_pix_im1[alpha_loc],
                cur_pix_im2[alpha_loc],
                cur_pix_im3[alpha_loc],
            )
            if alpha != 0:
                img1pix[row, col] = BLACK
    return image1

if __name__ == "__main__":
    main()
