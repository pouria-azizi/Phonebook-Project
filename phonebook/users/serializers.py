from django.contrib.auth import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            'pk',
            'first_name',
            'last_name',
            'username'
        ]
