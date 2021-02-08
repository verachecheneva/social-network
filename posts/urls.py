from django.urls import path

from .views import index, group_posts, new_post, profile, post_view, post_edit, add_comment, \
    follow_index, profile_unfollow, profile_follow


urlpatterns = [
    path("", index, name="index"),
    path("group/<slug:slug>/", group_posts, name="group"),
    path("new/", new_post, name="new_post"),
    path("follow/", follow_index, name="follow_index"),
    path("<str:username>/", profile, name="profile"),
    path("<str:username>/<int:post_id>/", post_view, name="post"),
    path("<str:username>/<int:post_id>/edit/", post_edit, name="post_edit"),
    path("<str:username>/<int:post_id>/comment", add_comment, name="add_comment"),
    path("<str:username>/follow/", profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", profile_unfollow, name="profile_unfollow"),
]
