
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<int:user_id>", views.profile_view, name="profile"),
    path("register", views.register, name="register"),
    path("following", views.following_view, name="following"),
    path("follow", views.follow, name="follow"),
    path("add_post", views.add_post, name="add_post"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("like", views.like, name="like"),
    path("removelike", views.removelike, name="removelike"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("save_post/<int:post_id>", views.save_post, name="save_post")
]
