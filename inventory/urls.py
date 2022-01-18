from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("objekt/", views.ObjektListView.as_view(), name="objekt-list"),
    path("objekt/add/", views.ObjektCreateView.as_view(), name="objekt-create"),
    path("objekt/<int:pk>/", views.ObjektDetailView.as_view(), name="objekt-detail"),
    path(
        "objekt/<int:pk>/change/",
        views.ObjektUpdateView.as_view(),
        name="objekt-update",
    ),
    path(
        "objekt/<int:pk>/delete/",
        views.ObjektDeleteView.as_view(),
        name="objekt-delete",
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
