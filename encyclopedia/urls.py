from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("add", views.add, name="add"),
    path("saved", views.saved, name="saved"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search")
]
