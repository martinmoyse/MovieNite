from django.urls import path
from . import views

from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("list", views.mylists_view, name="mylist"),
    path("explore", views.explore_view, name="explore"),
    path("match", views.match_view, name="match"),
    path("delete_from_list", views.delete_from_list, name="deletefromlist"),
    #path("search_by_title", views.search_by_title, name="searchbytitle")
]