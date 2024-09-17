from django.shortcuts import render
from django.views import View
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_backends
from .forms import CustomUserCreationForm

# This is a little complex because we need to detect when we are
# running in various configurations


class HomeView(View):
    def get(self, request):
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal
        }
        return render(request, 'home/main.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the correct backend as a string
            backend = 'django.contrib.auth.backends.ModelBackend'  # Use Django's default backend

            # Log in the user with the specified backend
            login(request, user, backend=backend)

            # Redirect to the login page after registration
            return redirect('/accounts/login/?next=' + request.POST.get('next', ''))  # Redirect to login with `next`
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
