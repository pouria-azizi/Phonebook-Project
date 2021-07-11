from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


class TestsUser(TestCase):

    def setUp(self):
        User.objects.create(username="pouryaa", password="pa123456")
        self.client = Client()

    def test_login(self):
        response = self.client.post("/users/login/",
                                    {
                                        'username': 'pouryaa',
                                        'password': 'pa123456'
                                    })

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        pass

    # def test_login(self):
    #     # First check for the default behavior
    #     response = self.client.get('/phones/')
    #     self.assertRedirects(response, '/users/login/')
    #
    #     # Then override the LOGIN_URL setting
    #     with self.settings(LOGIN_URL='/other/login/'):
    #         response = self.client.get('/phones/')
    #         self.assertRedirects(response, '/users/login/')