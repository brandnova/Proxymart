from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from core.models import SiteSettings
from .models import Profile

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

    user = request.user

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)  

    return render(request, 'accounts/home.html', {
        'profile': profile,
        'site_settings': site_settings,
    })

@login_required
def profile(request):
    site_settings = SiteSettings.objects.first()
    user = request.user

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)  

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        

        if profile_form.has_changed() and profile_form.is_valid():
            profile_form.save()
        else:
            profile_form = ProfileUpdateForm(instance=profile)

        
    else:
        profile_form = ProfileUpdateForm(instance=profile)
        user_form = UserUpdateForm(instance=user)


    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'profile_form': profile_form,
        'site_settings': site_settings,
    })

@login_required
def user_info_update(request):
    site_settings = SiteSettings.objects.first()
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user_form.has_changed() and user_form.is_valid():
            user_form.save()
        else:
            user_form = UserUpdateForm(instance=user)

        return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)

    return render(request, 'accounts/user_info_update.html', {
        'profile': profile,
        'user_form': user_form,
        'site_settings': site_settings,
    })

def user_logout(request):
    logout(request)
    return redirect(reverse('login'))