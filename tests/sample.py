"""
    Sample Functions
"""

from datetime import datetime

base_url = "http://127.0.0.1:5000"
post_url = f"{base_url}/api/posts"
author_url = f"{base_url}/api/authors"
media_url = f"{base_url}/api/media"
user_url = f"{base_url}/api/user"
category_url = f"{base_url}/api/categories"
poll_url = f"{base_url}/api/polls"

# MOCK DATA


def make_mock_article(authorId='1', id='1', title='A Test Article', cover_img='1', category=None):
    """Create Mock Article"""
    mock_cover = cover_img or make_mock_media()
    mock_author = authorId or make_mock_author()
    mock_category = category or make_mock_category()
    mock_post = {
        'postId': id,
        'title': title,
        'date': datetime.utcnow().isoformat(),
        'content': "A Test Publication",
        'author': authorId,
        'cover_image': cover_img,
        "categories": category,
        'type': 'article'
    }
    return mock_post


def make_mock_author(id='1', name='A Test Author', media_id='20'):
    mock_request = {
        'authorId': id,
        'name': name,
        'profile_image': media_id,
        'title': ['author', 'administrator', 'staff_writer'],
        'description': f'Hi, I am a test author #{id}'
    }
    return mock_request


def make_mock_media(id='1', title='Super Cool Pic', source="https://bit.ly/2xF5t73"):
    """Make media mock request"""
    mock_request = {
        'mediaId': id,
        'source': source,
        'credits': '@123ABC Comp.',
        'caption': 'Super Cool Image',
        'title': title,
        'type': 'cover-image'
    }
    return mock_request


def make_mock_profile_image(id='20', name='Braden Mars'):
    """make mock profile image"""
    mock_request = {
        "mediaId": id,
        "source": "https://s.hswstatic.com/gif/landscape-photography-1.jpg",
        "title": name,
        "type": "profile-image"
    }
    return mock_request


def make_mock_feedback(guest=True):
    """mock user feedback"""
    mock_request = {
        'phone': '7694561986',
        'subject': 'Cool New Idea',
        'content': 'wow more detail',
        'create_date': datetime.utcnow().isoformat(),
    }
    return mock_request


def make_mock_category(id='1', name='News'):
    """mock category data"""
    mock_request = {
        'categoryId': id,
        'name': name
    }
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
