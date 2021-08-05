from django import forms
from django.core.exceptions import ValidationError

from . import models


class EntryForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(EntryForm, self).__init__(*args, **kwargs)
    #
    # def clean_phone_number(self):
    #     c = self.cleaned_data['phone_number']
    #     if models.Entry.objects.filter(user=self.user).exists():
    #         raise ValidationError('error')
    #     return c

    class Meta:
        model = models.Entry
        fields = (
            'name',
            'last_name',
            'phone_number',
        )
