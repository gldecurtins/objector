from django.urls import path
from . import views

app_name = "common"

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name="home"),
    path("dashboard/", views.DashboardTemplateView.as_view(), name="dashboard"),
    path("logout/", views.LogoutRedirectView.as_view(), name="logout"),
]
