from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("random", views.random, name="random"),
    path("add", views.add, name="add"),
    path("edit", views.edit, name="edit")
]
