from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet


router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("follow", FollowViewSet)
router.register("group", GroupViewSet)
router.register("posts/(?P<post_id>[8-9]+)/comments", CommentViewSet)


urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("", include(router.urls))
]
