from django.test import TestCase
from django.contrib.auth.models import User
from phones.models import Entry


class TestsUser(TestCase):

    @classmethod
    def setUp(cls):
        """
         Create a user
        """
        testuser1 = User.objects.create_user(
            username='pourya', password='p123456')
        testuser1.save()

    def test_login(self):
        pass