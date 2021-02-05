from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Post, Group
from .forms import PostForm


def index(request):
    post_list = Post.objects.select_related("group").order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
        return render(request, "new_post.html", {"form": form})
    form = PostForm()
    return render(request, "new_post.html", {"form": form})


User = get_user_model()


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(author=author).order_by("-pub_date")
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"page": page, "author": author})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(author=author).order_by("-pub_date")
    num = posts_list.count()
    post = get_object_or_404(Post, author=author, id=post_id)
    return render(request, "post.html", {"num": num, "post": post,
                                         "author": author})


@login_required()
def post_edit(request, username, post_id):
    if username != request.user.username:
        return redirect(post_view, username, post_id)
    else:
        author = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, author=author, id=post_id)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect(post_view, username, post_id)
            return render(request, "new_post.html", {"form": form, "post": post})
        form = PostForm(instance=post)
        return render(request, "new_post.html", {"form": form, "post": post})
