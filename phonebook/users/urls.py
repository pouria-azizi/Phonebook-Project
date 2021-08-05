from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router3 = DefaultRouter()
router3.register('phones', views.UserViewSet)

app_name = 'users'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.EditUserProfile.as_view(), name='edit-profile'),
    path('api/v3/', include(router3.urls)),
]
