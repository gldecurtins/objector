from django.urls import path
from . import views

app_name = "maintenance"

urlpatterns = [
    path("work/", views.WorkListView.as_view(), name="work-list"),
    path("work/add/", views.WorkCreateView.as_view(), name="work-create"),
    path("work/<int:pk>/", views.WorkDetailView.as_view(), name="work-detail"),
    path("work/<int:pk>/change/", views.WorkUpdateView.as_view(), name="work-update"),
    path("work/<int:pk>/delete/", views.WorkDeleteView.as_view(), name="work-delete"),
    path(
        "work/<int:pk>/journal/add",
        views.WorkJournalCreate.as_view(),
        name="work-journal-create",
    ),
]
