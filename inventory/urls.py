from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("object/", views.ObjectListView.as_view(), name="object-list"),
    path("object/add/", views.ObjectCreateView.as_view(), name="object-create"),
    path("object/<int:pk>/", views.ObjectDetailView.as_view(), name="object-detail"),
    path(
        "object/<int:pk>/change/",
        views.ObjectUpdateView.as_view(),
        name="object-update",
    ),
    path(
        "object/<int:pk>/delete/",
        views.ObjectDeleteView.as_view(),
        name="object-delete",
    ),
    path("location/", views.LocationListView.as_view(), name="location-list"),
    path("location/add/", views.LocationCreateView.as_view(), name="location-create"),
    path(
        "location/<int:pk>/", views.LocationDetailView.as_view(), name="location-detail"
    ),
    path(
        "location/<int:pk>/change/",
        views.LocationUpdateView.as_view(),
        name="location-update",
    ),
    path(
        "location/<int:pk>/delete/",
        views.LocationDeleteView.as_view(),
        name="location-delete",
    ),
]
