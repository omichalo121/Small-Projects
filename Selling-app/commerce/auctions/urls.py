from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("archive", views.archive, name="archive"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watch", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("auctions", views.auctions, name="auctions"),
    path("bid", views.bid, name="bid"),
    path("delete", views.delete, name="delete"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:search>", views.category, name="category")
]