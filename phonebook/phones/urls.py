from django.urls import path
from . import views

app_name = 'phones'
urlpatterns = [
    path('create/', views.CreateEntry.as_view(), name='create'),
    path('find/', views.FindEntry.as_view(), name='find'),
    path('search/', views.ShowSearchForm.as_view(), name='search'),
    path('', views.ShowAddEntryForm.as_view(), name='show-add-entry-form'),
    path("contacts/", views.ContactList.as_view(), name="contacts"),
    # path("edit-contacts/", views.EditContact.as_view(), name="edit-contacts"),
    path('update/<int:pk>', views.EditContact.as_view(), name="edit-contacts"),
    path('activities/', views.SessionView.as_view(), name="recent-activities"),
    path('print/<int:pk>', views.PrintList.as_view(), name='print-list'),
]
