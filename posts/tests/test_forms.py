import shutil
import tempfile

from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.forms import PostForm
from myback import settings


class StaticURLTests(TestCase):
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
