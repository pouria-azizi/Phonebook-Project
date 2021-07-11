from django.test import TestCase
from phones.models import models
from . import views, forms


class PhoneTestCase(TestCase):
    """
    Test for phones view
    """
    def setUp(self):
        # Client.logine(
        models.Entry.objects.create(
            name='test',
            last_name='testiii',
            phone_number='09384641699'
        )

    def test_CreateEntry(self):
        obj = models.Entry
        phonnum = obj.phone_number
        self.assertContains(phonnum, '09')