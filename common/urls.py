from django.urls import path
from . import views

app_name = "common"

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name="home"),
    path("dashboard/", views.DashboardTemplateView.as_view(), name="dashboard"),
    path("logout/", views.LogoutRedirectView.as_view(), name="logout"),
    path("team/", views.TeamListView.as_view(), name="team-list"),
    path("team/add/", views.TeamCreateView.as_view(), name="team-create"),
    path("team/<int:pk>/", views.TeamDetailView.as_view(), name="team-detail"),
    path("team/<int:pk>/change/", views.TeamUpdateView.as_view(), name="team-update"),
    path("team/<int:pk>/delete/", views.TeamDeleteView.as_view(), name="team-delete"),
    path(
        "team/<int:pk>/member/add/",
        views.TeamMemberCreateView.as_view(),
        name="team-member-create",
    ),
    path(
        "team/<int:pk>/member/<int:user_id>/delete/",
        views.TeamMemberDeleteView.as_view(),
        name="team-member-delete",
    ),
]
