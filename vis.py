from pytagcloud import create_tag_image, make_tags
from yahoo_passwords import YAHOO_PASSWORDS

tags = make_tags(YAHOO_PASSWORDS, maxsize=120)

create_tag_image(tags, 'cloud_large.png', size=(900, 600), fontname='Lobster')
