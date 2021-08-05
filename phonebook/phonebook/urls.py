"""phonebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from phones import views as phones_views
from users import views as users_views

router = DefaultRouter()
router.register('phones', phones_views.UpdateContactViewSet)
router.register('users', users_views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('phones/', include('phones.urls')),
    path('users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
