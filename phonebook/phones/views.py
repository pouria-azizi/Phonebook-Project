import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.views.generic.edit import FormView, DeleteView
from rest_framework.exceptions import NotAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import permissions as permissionss
from . import forms, models
from .models import Entry
import weasyprint
from rest_framework import generics, viewsets, filters, status
from . import serializers
from . import permissions


logger = logging.getLogger(__name__)  # logger object


@method_decorator(csrf_exempt, name='dispatch')
class CreateEntry(LoginRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):

        form_instance = forms.EntryForm(data=self.request.POST)
        request.session['phone_number'] = models.Entry.phone_number
        if form_instance.is_valid():
            form_instance.save(commit=False).user = self.request.user
            entry_object = form_instance.save()
            request.session['create entry'] = 'create entry'
            request.session.modified = True
            # print(dict(request.session))
            logger.info(f'New contact is created by {self.request.user}')
            return JsonResponse(data={
                'success': True,
                'pk': entry_object.pk,
                'name': entry_object.name,
                'last_name': entry_object.last_name,
                'phone_number': entry_object.phone_number,
            }, status=201)
        else:
            request.session['error create entry'] = 'error create entry'
            request.session.modified = True
            logger.info(f'Failed create new contact by {self.request.user}')
            return JsonResponse(data={
                'success': False,
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ShowAddEntryForm(FormView):
    """
    Show the add entry form page
    """
    form_class = forms.EntryForm
    template_name = 'phones/add_entry.html'


class ShowSearchForm(TemplateView):
    """
    Show the search form page
    """
    template_name = 'phones/search.html'


@method_decorator(login_required, name='dispatch')
class FindEntry(generic.View):
    """
    Finds a phonebook entry
    """

    def get(self, request, *args, **kwargs):

        phone_number = self.request.GET.get('phonenum', None)
        value = self.request.GET.get('value', None)
        request.session['search'] = 'search'
        request.session.modified = True
        logger.info(f'Searching on phonebook by {self.request.user}')
        if not phone_number:
            return JsonResponse({'success': False, 'error': 'No number specified.'}, status=400)

        if value == 'Contain':
            qs = Entry.objects.filter(phone_number__contains=phone_number)

        elif value == 'Exact':
            qs = Entry.objects.filter(phone_number__exact=phone_number, user=self.request.user)

        elif value == 'StartWith':
            qs = Entry.objects.filter(phone_number__startswith=phone_number, user=self.request.user)

        elif value == 'EndWith':
            qs = Entry.objects.filter(phone_number__endswith=phone_number, user=self.request.user)

        return JsonResponse(
            {
                'results': list(
                    qs.values()
                ),
                'count': qs.count()
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class ContactList(ListView):
    """
    Show the list of contacts
    """
    model = models.Entry
    paginate_by = 6
    template_name = 'phones/entry_list.html'

    def get_queryset(self):
        self.request.session['show list'] = 'show list'
        self.request.session.modified = True
        logger.info(f'View contact list')
        return Entry.objects.filter(user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class EditContact(LoginRequiredMixin, UpdateView):
    model = models.Entry
    fields = (
        'name',
        'last_name',
        'phone_number',)
    template_name = 'phones/Entry_update_form.html'
    success_url = reverse_lazy('phones:contacts')

    def form_invalid(self, form):
        return HttpResponse(status=404)


class DeleteRow(DeleteView):
    model = models.Entry
    success_url = reverse_lazy('phones:contacts')


class SessionView(View):
    template_name = 'phones/phone_activate.html'

    def get(self, request, *args, **kwargs):
        # i = 0
        s = dict(request.session)
        # for key, value in dict(request.session).items():
        #     print(key, value)
        #     if i > 2:
        #         s[key] = value
        #         i += 1
        context = {
            'session': s
        }
        # print(s)
        return render(request, self.template_name, context=context)


class PrintList(LoginRequiredMixin, ListView):
    model = models.Entry
    template_name = 'phones/entry_detail.html'

    def get(self, request, *args, **kwargs):
        g = super(PrintList, self).get(request, *args, **kwargs)
        rendered_content = g.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        return response

    def get_queryset(self):
        qs = super().get_queryset()
        logger.info(f'Downloaded the list of contact as a pdf file by {self.request.user}')
        return qs.filter(user=self.request.user)


"""
REST Views
"""


class ContactListAPI(generics.ListAPIView):
    """
    Rest view for list of contact
    """
    queryset = models.Entry.objects.all()
    serializer_class = serializers.PhonesSerializers
    # permission_classes = [permissions.IsOwnerOrReadOnly]

    # def filter_queryset(self, queryset):
    #     return queryset.filter(user=self.request.user)
    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return Entry.objects.filter_by_user(user=self.request.user)


class CreateContactAPI(viewsets.ModelViewSet):
    """
    Rest view for create new contact
    """
    queryset = models.Entry.objects.all()
    serializer_class = serializers.PhonesSerializers
    # permission_classes = [permissions.IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return Entry.objects.filter_by_user(user=self.request.user)


class SearchAPI(generics.ListAPIView):
    """
    Rest view for search in phonebook
    """
    queryset = models.Entry.objects.all()
    serializer_class = serializers.PhonesSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_number']
    # permission_classes = [permissions.IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return Entry.objects.filter_by_user(user=self.request.user)


class UpdateContactViewSet(viewsets.ModelViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.UpdateSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_number']
    pagination_class = PageNumberPagination
    # permission_classes = [permissions.IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return Entry.objects.filter_by_user(user=self.request.user)

    # def get_object(self):
    #     try:
    #         return models.Entry.objects.get()
    #     except models.Entry.DoesNotExist:
    #         raise Http404

    # def get(self, request):
    #     qs = self.get_object()
    #     serializer = serializers.UpdateSerializer(qs, many=True)
    #     return Response(serializer.data)

    # def put(self, request):
    #     qs = self.get_object()
    #     serializer = serializers.UpdateSerializer(qs, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super().update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.phone_number = request.data.get('phone_number')
    #     instance.save()
    #
    #     serializer = self.get_serializer(instance)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

#
# class UpdateContactViewSet2(viewsets.ModelViewSet):
#     queryset = models.Entry.objects.all()
#     serializer_class = serializers.UpdateSerializer
#     # permission_classes = [permissions.IsOwnerOrReadOnly]
#
#     def get_queryset(self):
#         if self.request.user.is_anonymous:
#             raise NotAuthenticated('You need to be logged on.')
#         return Entry.objects.filter_by_user(user=self.request.user)
#
#     def put(self, request, pk):
#         qs = self.get_object()
#         serializer = serializers.UpdateSerializer(qs, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
