from django.urls import path

from .views import index, group_posts, new_post


urlpatterns = [
    path("", index, name="index"),
    path("group/<slug:slug>/", group_posts),
    path("new/", new_post, name="new_post"),
]
