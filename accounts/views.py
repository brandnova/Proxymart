from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import SiteSettings

def register(request):
    site_settings = SiteSettings.objects.first()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {
        'form': form,
        'site_settings': site_settings,
        })


def login(request):
    site_settings = SiteSettings.objects.first()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'site_settings': site_settings,
        })

@login_required
def home(request):
    site_settings = SiteSettings.objects.first()

    return render(request, 'accounts/home.html', {
        'site_settings': site_settings,
    })