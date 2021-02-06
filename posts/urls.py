from django.urls import path

from .views import index, group_posts, new_post, profile, post_view, post_edit, add_comment


urlpatterns = [
    path("", index, name="index"),
    path("group/<slug:slug>/", group_posts, name="group"),
    path("new/", new_post, name="new_post"),
    path("<str:username>/", profile, name="profile"),
    path("<str:username>/<int:post_id>/", post_view, name="post"),
    path("<str:username>/<int:post_id>/edit/", post_edit, name="post_edit"),
    path("<str:username>/<int:post_id>/comment", add_comment, name="add_comment"),
]
