from django.urls import path
from user_profile.views import (
    login_view,
    signup_view,
    home_view,
    logout_view,
    profile_view,
    dashboard_view,
    task_view,
    get_user_points,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login-user'),
    path('signup/', signup_view, name='signup-user'),
    path('logout/', logout_view, name='logout-user'),
    path('profile/', profile_view, name='profile-user'),
    path('dashboard/', dashboard_view, name='dashboard-user'),
    path('task/', task_view, name='task-user'),
    path('get_user_points/', get_user_points, name='points-user'),
]