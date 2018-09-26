"""
    warriorbeat/webhooks/wordpress/parse.py
    Parsing for wordpress webhook
"""

from webargs.flaskparser import parser
import requests


@parser.location_handler('wp:post')
def parse_post(request, name, field):
    """Parse wordpress webhook for a new post"""
    def get_ref(data, ref_key):
        """get reference data from a post"""
        ref = data['_links']
        item_ref = ref[ref_key][0]['href']
        item_request = requests.get(item_ref)
        item_data = item_request.json()
        return item_data
    data = request.form
    post_id = data['ID']
    post_request = requests.get(
        f"http://localhost:8000/wp-json/wp/v2/posts/{post_id}")
    _post_data = post_request.json()
    post_data = {
        'post': _post_data,
        'author': get_ref(_post_data, 'author'),
        'cover_img': get_ref(_post_data, 'wp:featuredmedia')
    }
    return post_data
