"""
    Sample Functions
"""

post_url = "http://127.0.0.1:5000/api/posts"
author_url = "http://127.0.0.1:5000/api/authors"
media_url = "http://127.0.0.1:5000/api/media"

# MOCK DATA


def make_mock_article(author=None, id='1', title='A Test Article', cover_img=None):
    """Create Mock Article"""
    mock_cover = cover_img or make_mock_media()
    mock_author = author or make_mock_author()
    mock_post = {
        'postId': id,
        'title': title,
        'author': {
            'authorId': mock_author['authorId'],
            'name': mock_author['name']
        },
        'type': 'article',
        'cover_image': mock_cover,
        'content': 'Filler Content!'
    }
    return mock_post


def make_mock_author(id='1', name='A Test Author'):
    mock_profile = {
        'name': name,
        'source': 'https://bit.ly/2QmP0eM',
        'mediaId': '9'
    }
    mock_author = {
        'authorId': id,
        'name': name,
        'profile_image': mock_profile,
        'posts': [],
        'title': 'Staff Writer',
        'description': f'Hi, I am a test author #{id}'
    }
    return mock_author


def make_mock_media(id='1', title='Super Cool Pic'):
    """Make media mock request"""
    mock_request = {
        'mediaId': id,
        'source': 'https://bit.ly/2xF5t73',
        'credits': '@123ABC Comp.',
        'caption': 'Super Cool Image',
        'title': title
    }
    return mock_request
# ----


def make_fullmock_article(id='10', title='A Cascading Article'):
    """article mock with full author and media details"""
    media = make_mock_media()
    author = make_mock_author(id='2')
    post = make_mock_article()
    post['author'] = author
    post['cover_image'] = media
    return post
