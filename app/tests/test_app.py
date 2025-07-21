import os 
os.environ["TESTING"] = "true"

import unittest
from peewee import SqliteDatabase
from app import app, TimelinePost, mydb

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.test_db = SqliteDatabase(':memory:')

        TimelinePost._meta.database = self.test_db

        self.test_db.connect()
        self.test_db.create_tables([TimelinePost])
    
    # helper functions to simplify the words needed to type for status code checking
    def assert_200_check(self, status_check):
        assert status_check.status_code == 200
    def assert_400_check(self, status_check):
        assert status_check.status_code == 400

    def test_home(self):
        response = self.client.get("/")
        self.assert_200_check(response)
        html = response.get_data(as_text=True)
        # print(html)
        assert "<title>MLH Fellow</title>" in html
    
    def test_get_timeline(self):
        response = self.client.get("/api/timeline_post")
        # true if the api end points returns http status 200
        print("Status code:", response.status_code)
        print("Response text:", response.get_data(as_text=True))
        self.assert_200_check(response)
        assert response.is_json # check if it's json being returned 
        json = response.get_json() # stores json into a variable
        assert len(json['timeline_posts']) == 0

    def get_response_data(self, response):
        """Helper method to get both text and JSON from response"""
        text_data = response.get_data(as_text=True)
        print("Response text:", text_data)
        json_data = response.get_json() if response.is_json else None
        return text_data, json_data


    def test_post_timeline_post(self):
        response = self.client.post('/api/timeline_post', data={
            'name': 'john bob',
            'email': 'bob@gmail.com',
            'content': 'bob was here',
        })

        print("Status code: ", response.status_code)
        self.assert_200_check(response)
        assert response.is_json

        text_data, json_data = self.get_response_data(response)

        # Verifying the posted data 
        assert json_data['name'] == 'john bob'
        assert json_data['email'] == 'bob@gmail.com'
        assert json_data['content'] == 'bob was here'
        assert 'id' in json_data
        assert 'created_at' in json_data

    def test_delete_timeline_post(self):
        # we'll first create a post
        post_response = self.client.post('/api/timeline_post', data={
            'name':'bob',
            'email': 'bob@gmail.com',
            'content': 'testing delete post',
        })
        self.assert_200_check(post_response)
        # testing to see what is being outputted
        post_text_data , post_json_data = self.get_response_data(post_response)
    
        #print("post text data: ",post_text_data)     
        #print("post json data: ",post_json_data)

        # Getting the post id first
        post_id = post_json_data['id']
        
        delete_request = self.client.delete(f'/api/timeline_post/{post_id}')
        delete_text_data, delete_json_data = self.get_response_data(delete_request)
        
        print("delete text_data: ", delete_text_data)
        print("delete json_data: ", delete_json_data)

        self.assert_200_check(delete_request)
        
        # verify if the deleted post data matches with what we created
        assert delete_json_data['id'] == post_id
        assert delete_json_data['name'] == 'bob'
        assert delete_json_data['email'] == 'bob@gmail.com'

    def test_email_format_post(self):
        # checking edge cases for users to submit a post request with an invalid email
        invalid_response = self.client.post("/api/timeline_post",data={
            'name':"bob",
            'email':'not-an-email', # does not contain `@`
            'content':"double content"
        })
        
        invalid_response_data, invalid_json_data = self.get_response_data(invalid_response)
        print("Invalid email response: ", invalid_response_data)
        self.assert_400_check(invalid_response)



    def test_empty_name_post(self):
        invalid_name_response = self.client.post("/api/timeline_post", data={
            'name':'',
            'email':'hi@gmail.com',
            'content': 'testing empty name',
        })

        invalid_name_response_data , invalid_json_data = self.get_response_data(invalid_name_response)

        print("Can't have an empty name: ", invalid_name_response_data)

        self.assert_400_check(invalid_name_response)
