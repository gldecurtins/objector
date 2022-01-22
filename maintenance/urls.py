from django.urls import path
from . import views

app_name = "maintenance"

urlpatterns = [
    path("task/", views.TaskListView.as_view(), name="task-list"),
    path(
        "object/task/add/",
        views.TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "object/<int:object_id>/task/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "object/<int:object_id>/task/<int:pk>/change/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "object/<int:object_id>/task/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path(
        "object/journal/add",
        views.JournalCreate.as_view(),
        name="journal-create",
    ),
    path(
        "object/<int:object_id>/journal/<int:pk>/",
        views.JournalDetailView.as_view(),
        name="journal-detail",
    ),
    path(
        "object/<int:object_id>/journal/<int:pk>/change/",
        views.JournalUpdateView.as_view(),
        name="journal-update",
    ),
    path(
        "object/<int:object_id>/journal/<int:pk>/delete/",
        views.JournalDeleteView.as_view(),
        name="journal-delete",
    ),
]
