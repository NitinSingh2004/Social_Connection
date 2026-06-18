from django.urls import path
from . import views

urlpatterns = [

    # Real-time backend validation checkers called by JavaScript
    path('accounts/check-email/', views.check_email, name='check_email'),
    path('accounts/check-username/', views.check_username, name='check_username'),



    path(
        "signup/",
        views.signup_view,
        name="signup"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "dashboard",
        views.dashboard_view,
        name="dashboard"
    ), 
    path(
        "password_reset/",
        views.password_reset,
        name="password_reset"
    )
]