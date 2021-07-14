import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from . import forms, models
logger = logging.getLogger(__name__)  # logger object


@csrf_exempt
def login_view(request):
    """
    Logins the user
    """
    user = None
    form_instance = forms.LoginForm()
    if request.method == 'POST':
        request.session['user login'] = 'user login'
        form_instance = forms.LoginForm(data=request.POST, files=request.FILES)
        if form_instance.is_valid():
            username = form_instance.cleaned_data['username']
            password = form_instance.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            logger.info(f'{user} is login')
            if user is not None:
                # The user was found and authenticated
                login(request, user)
                next_url = request.GET.get('next', '/')
                # Make sure we are only redirect to inter urls
                if is_safe_url(next_url, settings.ALLOWED_HOSTS):
                    return redirect('phones:show-add-entry-form')
                else:
                    return redirect('phones:show-add-entry-form')
            else:
                # The user or password is invalid
                messages.error(request, "Username or password was incorrect !!")

    return render(
        request,
        context={
            'form': form_instance
        },
        template_name='users/login.html'
    )


def logout_view(request):
    """
    Logs out the user
    """
    logout(request)
    logger.info(f'user is logout')
    return redirect('users:login')


#  View Class
class EditUserProfile(LoginRequiredMixin, UpdateView):
    """
    Updates a user profile
    """
    model = get_user_model()
    fields = (
        'first_name',
        'last_name',
        'email',
    )
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('phones:show-add-entry-form')

    def get_object(self, queryset=None):
        logger.info(f'updated profile by {self.request.user}')
        return self.request.user
