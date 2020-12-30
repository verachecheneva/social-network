from django.urls import path, include
from .views import index, group_posts


urlpatterns = [
    path('', index),
    path('group/<slug>/', group_posts)
    # path('accounts/sign-up', sign_up),
    # path('accounts/sign-in', sign_in),
    # path('accounts/my-account', my_account),
]
