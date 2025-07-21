import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):

        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)


    def tearDown(self):
        test_db.drop_tables(MODELS)
        
        # Close the connection to the database
        test_db.close()

    def test_timeline_post(self):
        # creating 2 timeline posts
        first_post = TimelinePost.create(name="bob", email="heybob@gmail.com", content="Hey bro, waddup")
        assert first_post.id == 1

        second_post = TimelinePost.create(name="johb", email="john@gmail.com", content="hey bro, yerrr")
        assert second_post.id == 2



