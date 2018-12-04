"""
    Sample Functions
"""

base_url = "http://127.0.0.1:5000"
post_url = f"{base_url}/api/posts"
author_url = f"{base_url}/api/authors"
media_url = f"{base_url}/api/media"
user_url = f"{base_url}/api/user"
category_url = f"{base_url}/api/categories"
poll_url = f"{base_url}/api/polls"

# MOCK DATA


def make_mock_article(author=None, id='1', title='A Test Article', cover_img=None, category=None):
    """Create Mock Article"""
    mock_cover = cover_img or make_mock_media()
    mock_author = author or make_mock_author()
    mock_category = category or make_mock_category()
    mock_post = {
        'postId': id,
        'title': title,
        'author': {
            'authorId': mock_author['authorId']
        },
        'categories': mock_category,
        'type': 'article',
        'cover_image': mock_cover,
        'content': 'Filler Content!',
        'date': '2018-11-13T21:23:13'
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
        'title': ['author', 'staff_writer'],
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


def make_mock_feedback(guest=True):
    """mock user feedback"""
    mock_request = {
        'phone': '7694561986',
        'subject': 'Cool New Idea',
        'content': 'wow more detail'
    }
    return mock_request


def make_mock_category(id='1', name='News'):
    """mock category data"""
    mock_request = [
        {
            'categoryId': id,
            'name': name
        }
    ]
    return mock_request


def make_mock_poll():
    """make mock poll data"""
    mock_request = {
        "pollId": "1",
        "question": "Yes or No?",
        "status": "Open",
        "date": "2018-10-11T08:55:57",
        "answers": [
            {
                "answerId": "0",
                "answer": "Yes",
                "votes": "5"
            },
            {
                "answerId": "1",
                "answer": "No",
                "votes": "3"
            }
        ]
    }
    return mock_request
# ----


def make_fullmock_article(id='10', title='A Cascading Article'):
    """article mock with full author and media details"""
    media = make_mock_media()
    author = make_mock_author(id='2')
    categories = make_mock_category()
    categories.extend(make_mock_category(
        id='2', name='Sports'))
    del author['posts']
    post = make_mock_article()
    post['author'] = author
    post['cover_image'] = media
    post['categories'] = categories
    return post
