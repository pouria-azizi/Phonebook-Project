from django.core.management import BaseCommand
from django.http import JsonResponse
from phones.models import Entry


class Command(BaseCommand):

    def handle(self, *args, **options):
        obj = Entry.objects.filter()
        return JsonResponse(
            data={
                 'name': obj.name,
                'last_name': obj.last_name,
                'phone_number': obj.phone_number,
            },
        )
