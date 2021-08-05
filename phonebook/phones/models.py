import logging
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels

phone_regex = RegexValidator(regex='^0[0-9]{2,}[0-9]{7,}$', message='phone number invalid')

logger = logging.getLogger(__name__)  # logger object


class ContactQuerySetManager(models.QuerySet):
    """
    Custom QuerySet manager for Entry model
    """
    def filter_by_user(self, user):
        """
        Filter objects by owner field
        """
        return self.filter(user=user)


class Entry(models.Model):
    """
    An entry in the phonebook
    """
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('تاریخ ثبت'))
    name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    phone_number = models.CharField(validators=[phone_regex], max_length=11, verbose_name=_('شماره تلفن'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name=_('کاربر'))

    objects = ContactQuerySetManager().as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone_number', 'user'], name='UniqueNumber')
        ]
