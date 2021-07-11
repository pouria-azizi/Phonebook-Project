from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

phone_regex = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='phone number invalid')


class Entry(models.Model):
    """
    An entry in the phonebook
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ثبت'))
    name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    phone_number = models.CharField(validators=[phone_regex], max_length=11, verbose_name=_('شماره تلفن'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name=_('کاربر'))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone_number', 'user'], name='UniqueNumber')
        ]
