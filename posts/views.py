from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Post, Group, Comment, User
from .forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.select_related("group").order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page}, content_type="text/html", status=200)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page}, content_type="text/html", status=200)


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


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(author=author).order_by("-pub_date")
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"page": page, "author": author}, content_type="text/html", status=200)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(author=author).order_by("-pub_date")
    num = posts_list.count()
    post = get_object_or_404(Post, author=author, id=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post=post)
    return render(request, "post.html", {"num": num, "post": post, "form": form, "comments": comments})


@login_required
def post_edit(request, username, post_id):
    if username != request.user.username:
        return redirect(post_view, username, post_id)
    else:
        author = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, author=author, id=post_id)
        if request.method == "POST":
            form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
            if form.is_valid():
                form.save()
                return redirect(post_view, username, post_id)
            return render(request, "new_post.html", {"form": form, "post": post})
        form = PostForm(instance=post)
        return render(request, "new_post.html", {"form": form, "post": post})


@login_required
def add_comment(request, username, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            post_author = get_object_or_404(User, username=username)
            comment.post = Post.object.filter(author=post_author).filter(id=post_id)
            comment.save()
            return redirect("post.html", username=username, post_id=post_id)
    form = CommentForm()
    return render(request, "post.html", {"username": username, "post_id": post_id, "form": form})


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
