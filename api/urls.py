from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register('posts', PostViewSet)

router_1 = DefaultRouter()
router_1.register('', CommentViewSet)

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("posts/<int:post_id>/comments/", include(router_1.urls)),
    path("", include(router.urls))
]
