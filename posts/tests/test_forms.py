import shutil
import tempfile
import time

from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, Group, User, Follow, Comment
from posts.forms import PostForm


class StaticFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.form = PostForm()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username="Vera")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(title="TestGroup", slug="TestGroup", description="Group description")
        Post.objects.create(text="This is text", author=cls.user, group=cls.group)
        cls.post = Post.objects.get(text="This is text")
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b')
        cls.image_post = SimpleUploadedFile(name='small.gif', content=small_gif, content_type='image/gif')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    """Проверим, что при отправке формы создается новая запись в БД"""
    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            "text": "Это новый пост",
            "group": self.group.id
        }
        response = self.authorized_client.post(reverse("new_post"), data=form_data, follow=True)
        self.assertRedirects(response, "/")
        self.assertEqual(Post.objects.count(), post_count+1)

    """Тест на изменение записи в БД при редактировании поста"""
    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            "text": "Пост изменен",
            "group": self.group.id
        }
        response = self.authorized_client.post(reverse("post_edit", kwargs={"username": "Vera", "post_id": 1}),
                                               data=form_data, follow=True)
        post = Post.objects.filter(author=self.user).get(id=1).text
        self.assertRedirects(response, "/Vera/1/")
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(post, "Пост изменен")

    """Проверим, что при отправке поста с картинкой создается новая запись в БД"""
    def test_create_post_with_image(self):
        post_count = Post.objects.count()
        form_data = {
            "text": "Пост с картинкой",
            "group": self.group.id,
            "image": self.image_post
        }
        response = self.authorized_client.post(reverse("new_post"), data=form_data, follow=True)
        self.assertRedirects(response, "/")
        self.assertEqual(Post.objects.count(), post_count + 1)


class TestFollower(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username="Vera")
        cls.user_1 = User.objects.create_user(username="Alina")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client_1 = Client()
        cls.authorized_client_1.force_login(cls.user_1)
        Post.objects.create(text="This is text", author=cls.user)
        cls.post = Post.objects.get(text="This is text")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    """Авторизованный пользователь может подписываться и отписываться"""
    def test_follow(self):
        count = Follow.objects.count()
        response = self.authorized_client.get(reverse("profile_follow", kwargs={"username": "Alina"}), follow=True)
        count_1 = Follow.objects.count()
        response = self.authorized_client.get(reverse("profile_unfollow", kwargs={"username": "Alina"}), follow=True)
        count_2 = Follow.objects.count()
        self.assertNotEqual(count, count_1)
        self.assertEqual(count, count_2)

    """Проверю, что неавторизованный пользователь не может комментироввать посты"""
    def test_guest_user_can_not_create_comments(self):
        form_data = {
            "text": "Пост с комментарием",
        }
        response = self.guest_client.get(reverse("add_comment", kwargs={"username": "Vera", "post_id": self.post.id}),
                                         data=form_data, follow=True)
        self.assertNotEqual(response, "/Vera/1/")

    """Проверю, что авторизованный пользователь может комментироввать посты"""
    def test_authorized_user_can_create_comments(self):
        comment_count = Comment.objects.count()
        form_data = {
            "text": "Это новый comment",
        }
        response = self.authorized_client.post(reverse("add_comment", kwargs={"username": "Vera", "post_id": 1}),
                                               data=form_data, follow=True)
        self.assertRedirects(response, "/Vera/1/")
        self.assertEqual(Comment.objects.count(), comment_count + 1)