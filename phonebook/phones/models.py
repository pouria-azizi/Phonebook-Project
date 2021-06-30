from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

phone_regex = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='phone number invalid')


class Entry(models.Model):
    """
    An entry in the phonebook
    """
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=11)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone_number', 'user'], name='UniqueNumber')
        ]
