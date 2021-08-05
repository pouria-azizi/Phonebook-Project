from rest_framework import serializers
from . import models


class PhonesSerializers(serializers.HyperlinkedModelSerializer):
    """
    Serializers class for phonebook
    """
    class Meta:
        model = models.Entry
        fields = [
            'name',
            'last_name',
            'phone_number'
        ]


class UpdateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Entry
        fields = [
            'pk',
            'name',
            'last_name',
            'phone_number'
        ]
#
#     def update(self, instance, validated_data):
#         instance = validated_data(data=models.Entry.phone_number)
#         return instance
