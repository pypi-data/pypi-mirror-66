from django import template
from django.utils.html import format_html
from ..conf import get_picsum_setting, get_pixabay_setting
from django.template.exceptions import TemplateSyntaxError
import requests
import random
register = template.Library()


def get_html(class_, img_id, formatted_url):
    formatted_html = ''
    if class_ and img_id:
        formatted_html = '<img src ={} class= {} id = {}>'.format(
            formatted_url, class_, img_id)
    elif class_:
        formatted_html = '<img src ={} class= {} >'.format(
            formatted_url, class_)
    elif img_id:
        formatted_html = '<img src ={} id ={} >'.format(formatted_url, img_id)
    else:
        formatted_html = '<img src ={}  >'.format(formatted_url)
    return formatted_html


@register.simple_tag
def pic_rand(*args, **kwargs):
    """
    :param width :  The width of the placeholder image required it is a required param
    :param height: 
    The height of  the image if you  need a square image passing width 
    is enough it is a optional param

    """
    height = kwargs.get('height')
    width = kwargs.get('width')
    id_ = kwargs.get('pic_id')
    class_ = kwargs.get("class")
    img_id = kwargs.get('id')

    formatted_url = None

    """
    Using format() to support all Python 3 Versions
    """
    _url = get_picsum_setting('url')
    _width_format = '{}{}/'
    _height_format = '{}{}/{}'
    if height and width and not id_:
        formatted_url = _height_format.format(_url, width, height)
    elif width and not id_:
        formatted_url = _width_format.format(_url, width)
    elif height and width and id_:

        formatted_url = '{0}/id/{1}/{2}/{3}'.format(_url, id_, width, height)
    elif height and id_:
        formatted_url = '{0}/id/{1}/{2}/'.format(_url, id_, height)
    formatted_html = get_html(class_, img_id, formatted_url)
    return format_html(formatted_html)


@register.simple_tag
def pix_image(*args, **kwargs):
    """
    It retrives the image from the officail Pixabay api https://pixabay.com/api/
    Make sure you declare 'PIXABAY_KEY' in your settings.py file

    Eg :PIXABAY_KEY = 'gfff'
 These are the list of params u can pass

q	A URL encoded search term. If omitted, all images are returned. This value may not exceed 100 characters.
Example: "yellow+flower"

lang	Language code of the language to be searched in.
Accepted values: cs, da, de, en, es, fr, id, it, hu, nl, no, pl, pt, ro, sk, fi, sv, tr, vi, th, bg, ru, el, ja, ko, zh
Default: "en"


image_type	Filter results by image type.
Accepted values: "all", "photo", "illustration", "vector"
Default: "all"

orientation	Whether an image is wider than it is tall, or taller than it is wide.
Accepted values: "all", "horizontal", "vertical"
Default: "all"

category	Filter results by category.
Accepted values: backgrounds, fashion, nature, science, education, feelings, health, people, religion, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music
min_width	Minimum image width.
Default: "0"

min_height	Minimum image height.
Default: "0"

colors	Filter images by color properties. A comma separated list of values may be used to select multiple properties.

Accepted values: "grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown"

editors_choice	Select images that have received an Editor's Choice award.

Accepted values: "true", "false"
Default: "false"

safesearch	A flag indicating that only images suitable for all ages should be returned.
Accepted values: "true", "false"
Default: "false"

order	How the results should be ordered.
Accepted values: "popular", "latest"
Default: "popular"

page	Returned search results are paginated. Use this parameter to select the page number.
Default: 1

per_page	Determine the number of results per page.
Accepted values: 3 - 200
Default: 20

callback	JSONP callback function name
pretty	Indent JSON output. This option should not be used in production.
Accepted values: "true", "false"
Default: "false"

    """

    key = get_pixabay_setting('key')
    _url = get_pixabay_setting('url')+'?key={}&'.format(key)

    class_, img_id = kwargs.get('class'), kwargs.get('id')
    if 'id' in kwargs:
        kwargs.pop('id')
    if 'class' in kwargs:
        kwargs.pop('class')
    for key, value in kwargs.items():   
        if key == 'img_d':
            _url += '{}={}&'.format('id', value)

        _url += '{}={}&'.format(key, value)

    res = requests.get(_url).json()
    hits = res.get('hits')
    img_url = hits[random.randint(0, len(hits))]['largeImageURL']
    print(img_url)
    formatted_html = get_html(class_, img_id, img_url)
    return format_html(formatted_html)
