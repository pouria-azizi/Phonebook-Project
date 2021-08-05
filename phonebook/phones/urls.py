from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router2 = DefaultRouter()
router2.register('phones', views.CreateContactAPI)
# router1 = DefaultRouter()
# router1.register('phones', views.ContactListAPI)
# router3 = DefaultRouter()
# router3.register('phones', views.UserViewSet)
router5 = DefaultRouter()
router5.register('phones', views.UpdateContactViewSet)

app_name = 'phones'
urlpatterns = [
    path('create/', views.CreateEntry.as_view(), name='create'),
    path('find/', views.FindEntry.as_view(), name='find'),
    path('search/', views.ShowSearchForm.as_view(), name='search'),
    path('', views.ShowAddEntryForm.as_view(), name='show-add-entry-form'),
    path("contacts/", views.ContactList.as_view(), name="contacts"),
    path('delete/<int:pk>', views.DeleteRow.as_view(), name='delete-from-phonebook'),
    path('update/<int:pk>', views.EditContact.as_view(), name="edit-contacts"),
    path('activities/', views.SessionView.as_view(), name="recent-activities"),
    path('print/', views.PrintList.as_view(), name='print-list'),
    path('api/v0/', views.ContactListAPI.as_view()),
    path('api/v2/', include(router2.urls)),
    # path('api/v3/', include(router3.urls)),
    path('api/v5/', include(router5.urls)),
    path('api/v4/', views.SearchAPI.as_view()),
    # path('api/v5/phones/<int:pk>', views.UpdateContactViewSet2.as_view({'get': 'put'}), name='api'),
]
