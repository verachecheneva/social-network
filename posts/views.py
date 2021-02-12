from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .models import Post, Group, Comment, User, Follow
from .forms import PostForm, CommentForm


@cache_page(20)
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
    following = Follow.objects.filter(author=author)
    user = request.user
    for follower in following:
        if follower.user == user:
            return render(request, "profile.html", {"page": page, "author": author, "following": following},
                          content_type="text/html")
    return render(request, "profile.html", {"page": page, "author": author}, content_type="text/html")


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    num_1 = Follow.objects.filter(author=author).count()
    num_2 = Follow.objects.filter(user=author).count()
    post = get_object_or_404(Post, author=author, id=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post=post)
    return render(request, "post.html", {"post": post, "author": author, "form": form, "comments": comments,
                                         "num_1": num_1, "num_2": num_2})


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
    post_author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=post_author, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(post_view, username=username, post_id=post_id)
    form = CommentForm()
    return redirect(add_comment, username=username, post_id=post_id, form=form)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"page": page}, content_type="text/html", status=200)


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user == author:
        return redirect(profile, username=username)
    following_exist = Follow.objects.filter(user=user, author=author).exists()
    if following_exist:
        return redirect(profile, username=username)
    Follow.objects.create(user=user, author=author)
    return redirect(profile, username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user == author:
        return redirect(profile, username=username)
    follow = get_object_or_404(Follow, user=user, author=author)
    follow.delete()
    return redirect(profile, username=username)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
