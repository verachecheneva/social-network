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
    title = "Добавить зпись"
    header = "Добавить запись"
    button = "Добавить"
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
        return render(request, "new_post.html", {"form": form, "title": title, "header": header, "button": button})
    form = PostForm()
    return render(request, "new_post.html", {"form": form, "title": title, "header": header, "button": button})


User = get_user_model()


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(username=username).order_by("-pub_date")
    num = posts_list.count()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"username": username, "page": page, "author": author, "num": num})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(username=username).order_by("-pub_date")
    num = posts_list.count()
    text = Post.objacts.filter(username=username).filter(post_id=post_id)
    return render(request, "post.html", {"username": username, "post_id": post_id, "num": num, "text": text,
                                         "author": author})


@login_required()
def post_edit(request, username, post_id):
    if username != request.User.username:
        author = get_object_or_404(User, username=username)
        posts_list = Post.objects.filter(username=username).order_by("-pub_date")
        num = posts_list.count()
        text = Post.objacts.filter(username=username).filter(post_id=post_id)
        return render(request, "post.html", {"username": username, "post_id": post_id, "num": num, "text": text,
                                             "author": author})
    else:
        title = "Редактировать зпись"
        header = "Редактировать запись"
        button = "Сохранить"
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect("index")
            return render(request, "new_post.html", {"form": form, "title": title, "header": header, "button": button})
        form = PostForm()
        return render(request, "new_post.html", {"form": form, "title": title, "header": header, "button": button})
