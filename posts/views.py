from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Group


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    return render(request, 'index.html', {'posts': posts})


def group_posts(request):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})
