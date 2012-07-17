from pytagcloud import create_tag_image, make_tags
from yahoo_passwords import YAHOO_PASSWORDS_SMALL
from billabong_paswords import BILLABONG_PASWORDS_SMALL
from myspace_passwords import MYSPACE_PASSWORDS_SMALL

yahoo_tags = make_tags(YAHOO_PASSWORDS_SMALL)
billabong_tags = make_tags(BILLABONG_PASWORDS_SMALL)
myspace_tags = make_tags(MYSPACE_PASSWORDS_SMALL, maxsize=120)

create_tag_image(yahoo_tags, 'cloud_yahoo.png', size=(900, 600), fontname='Lobster')
create_tag_image(billabong_tags, 'cloud_billabong.png', size=(900, 600), fontname='Lobster')
create_tag_image(myspace_tags, 'cloud_myspace.png', size=(900, 600), fontname='Lobster')

