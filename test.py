from unittest import TestCase
from app import app
from models import User, Post

class blogly_tests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with app.test_client() as client:
            res = client.get('/user')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_add_user_form(self):
        with app.test_client() as client:
            res = client.post('new_user', data={'first_name': 'Tracey'})
            html = res.get_data(as_text=True)

            self.assertTrue('Tracey')

    def test_add_post_form(self):
        with app.test_client() as client:
            res = client.post('new_post', data={'title': 'My First Post'})
            html = res.get_data(as_text=True)

            self.assertTrue('My First Post')

    

    


   