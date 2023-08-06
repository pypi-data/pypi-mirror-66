"""URL mappings for squarelet app"""

# Django
from django.urls import path

# SquareletAuth
from squarelet_auth import views

app_name = "squarelet_auth"
urlpatterns = [
    path("webhook/", views.webhook, name="webhook"),
    path("signup/", views.webhook, name="signup"),
    path("login/", views.webhook, name="login"),
    path("logout/", views.webhook, name="logout"),
]
