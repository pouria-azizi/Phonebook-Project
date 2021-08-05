# from django.test import TestCase
# from django.contrib.auth.models import User
# from .models import Entry
#
#
# class PhoneTestCase(TestCase):
#     """
#     Test for phones view
#     """
#
#     @classmethod
#     def setUpTestData(cls):
#
#         # Create a user
#         testuser1 = User.objects.create_user(
#             username='pourya', password='p123456')
#         testuser1.save()
#         # Create a blog post
#         test_post = Entry.objects.create(
#             user=testuser1, name='pourya', last_name='aziziiii', phone_number='09384641632')
#         test_post.save()
#
#     def test_phone_contact(self):
#
#         contact = Entry.objects.get(pk=1)
#         expected_user = f'{contact.user}'
#         expected_name = f'{contact.name}'
#         expected_last_name = f'{contact.last_name}'
#         expected_phone_number = f'{contact.phone_number}'
#         self.assertEqual(expected_user, 'pourya')
#         self.assertEqual(expected_name, 'pourya')
#         self.assertEqual(expected_last_name, 'aziziiii')
#         self.assertEqual(expected_phone_number, '09384641632')

from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from . import forms
from .forms import EntryForm
from .models import Entry


class AddEntryTestCase(TestCase):
    def setUp(self):
        pass

    def test_page_rendering(self):
        response_for_login_required = self.client.get(reverse('phones:create'))
        self.assertEqual(response_for_login_required.status_code, 302)
        response_for_page_rendering = self.client.get(reverse('phones:create'), follow=True)
        self.assertEqual(response_for_page_rendering.status_code, 200)

    def test_post_transfer(self):
        data = {}
        resp = self.client.post(reverse('phones:create'), data={
            'name': 'pourya',
            'last_name': 'azizi',
            'phone_number': '09384641631',
        }, content_type='application/x-www-form-urlencoded')

        self.assertEqual(resp.status_code, 302)

    def test_valid_form(self):
        entry = Entry.objects.create(name='pourya', last_name='azizi', phone_number='09384641631')
        data = {'name': entry.name, 'last_name': entry.last_name, 'phone_number': entry.phone_number}
        form = EntryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        entry = Entry.objects.create(name='zahra', last_name='hassani', phone_number='asdggsd')
        data = {'name': entry.name, 'last_name': entry.last_name, 'phone_number': entry.phone_number}
        form = EntryForm(data=data)
        self.assertFalse(form.is_valid())


class SearchEntryTestCase(TestCase):
    def setUp(self):
        pass

    def test_rendered_page(self):
        resp = self.client.get(reverse('phones:search'), follow=True)
        self.assertEqual(resp.status_code, 200)

        login = self.client.login(
            username='pourya',
            password='p123456',
        )
        self.assertTrue(login)

        resp = self.client.get(reverse('phones:search'), data={
            'phonenum': '09',
            'value': 'Contain'
        })
        self.assertEqual(resp.status_code, 200)


class ContactsTestCase(TestCase):
    def setUp(self):
        self.obj1 = Entry.objects.create(name='amir', last_name='amiri', phone_number='09135247885')
        self.obj2 = Entry.objects.create(name='ali', last_name='alavi', phone_number='09145247885')
        self.obj3 = Entry.objects.create(name='karim', last_name='karimi', phone_number='09195247885')

    def test_qs_filtering(self):
        pass


class EditEntryTestCase(TestCase):
    def setUp(self):
        pass


class ActivitiesHistoryTestCase(TestCase):
    def setUp(self):
        pass