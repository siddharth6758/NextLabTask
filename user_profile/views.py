import re

from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from user_profile.models import UserPoints
from app_track.models import Apps, UserAppInstall

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def home_view(request):
    return render(request,'base.html')

@login_required
@csrf_exempt
def get_user_points(request):
    try:
        val = UserPoints.objects.filter(user=request.user)
        points = 0
        if val.exists():
            points = val.first().points
        return JsonResponse({'points':points,'status':200})
    except Exception as e:
        print(f'\n\nError: {str(e)}\n\n')
        points = 0
        return JsonResponse({'points':points,'status':500})

def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname',None)
        lastname = request.POST.get('lastname',None)
        username = request.POST.get('username',None)
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        confirm_password = request.POST.get('confirm_password',None)

        if User.objects.filter(email=email).exists():
            messages.info(request,'Email ID already exists!')
            return redirect('signup-user')

        if password != confirm_password:
            messages.error(request,'Password and Confirm Password does not match!')
            return redirect('signup-user')

        if not password and not confirm_password:
            messages.error(request,'Please provide a Password...')
            return redirect('signup-user')

        user = User.objects.create(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request,'signup_page.html')

def login_view(request):
    if request.method == 'POST':
        email_username = request.POST.get('email_username',None)
        password = request.POST.get('password',None)
        user = None
        if re.fullmatch(email_regex, email_username):
            user_list = User.objects.filter(email=email_username)
            if user_list.exists():
                email_username = user_list.first().username
            else:
                messages.error(request,'Invalid Email/Username or Password...')
                return redirect('login-user')
        user = authenticate(request, username=email_username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Email/Username or Password...')
    return render(request, 'login_page.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname',None)
        lastname = request.POST.get('lastname',None)
        username = request.POST.get('username',None)
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        confirm_password = request.POST.get('confirm_password',None)
        user = User.objects.get(id=request.user.id)
        if password and confirm_password:
            if password != confirm_password:
                messages.error(request,'Password and Confirm Password does not match!')
                return redirect('profile-user')
            else:
                user.set_password(password)
                user.save()
                messages.success(request,'User password changed!')
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                return redirect('profile-user')

        user.first_name=firstname
        user.last_name=lastname
        user.username=username
        user.email=email
        user.save()
        messages.success(request,'User profile updated!')
        return redirect('profile-user')
    return render(request,'profile_page.html')

@login_required
def dashboard_view(request):
    apps = None
    if request.user.is_superuser:
        apps = Apps.objects.all()
    else:
        apps_list = UserAppInstall.objects.filter(user=request.user).values_list('app__id',flat=True)
        apps = Apps.objects.filter(id__in=apps_list)
    return render(request,'home_page.html',{
        'apps':apps
    })

@login_required
def task_view(request):
    user_apps = UserAppInstall.objects.filter(user=request.user).values_list('app__id',flat=True)
    pending_apps = Apps.objects.exclude(id__in=user_apps)
    print(pending_apps)
    return render(request,'task_page.html',{
        'pending_apps':pending_apps
    })