import shutil
import tempfile

from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from posts.models import Post, Group, User


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username="Vera")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(title="TestGroup", slug="TestGroup", description="Group description")
        Post.objects.create(text="This is text", author=cls.user, group=cls.group)
        cls.post = Post.objects.get(text="This is text")
        cls.user_1 = User.objects.create_user(username="Alina")
        cls.other_client = Client()
        cls.other_client.force_login(cls.user_1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Рекурсивно удаляем временную после завершения тестов
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    """Тестируем шаблон, получаемый при обращении к view-функции через name"""
    def test_index_page_uses_correct_template(self):
        response = self.guest_client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")

    def test_NewPost_page_uses_correct_template(self):
        response = self.authorized_client.get(reverse("new_post"))
        self.assertTemplateUsed(response, "new_post.html")

    def test_group_page_uses_correct_template(self):
        response = self.guest_client.get(reverse("group", kwargs={"slug": self.group.slug}))
        self.assertTemplateUsed(response, "group.html")

    """Тест на соответствие словаря context, передаваемого в шаблон при вызове, с ожидаемым"""
    def test_index_page_show_correct_context(self):
        response = self.guest_client.get(reverse("index"))
        task_text_0 = response.context.get("page")[0].text
        task_group_0 = response.context.get("page")[0].group
        self.assertEqual(task_text_0, "This is text")
        self.assertEqual(task_group_0, self.group)

    def test_group_page_show_correct_context(self):
        response = self.guest_client.get(reverse("group", kwargs={"slug": self.group.slug}))
        task_text_0 = response.context.get("page")[0].text
        task_group_0 = response.context.get("page")[0].group
        task_title_group = response.context.get("group").title
        task_description_group = response.context.get("group").description
        self.assertEqual(task_text_0, "This is text")
        self.assertEqual(task_group_0, self.group)
        self.assertEqual(task_title_group, self.group.title)
        self.assertEqual(task_description_group, self.group.description)

    def test_NewPost_page_show_correct_context(self):
        response = self.authorized_client.get(reverse("new_post"))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    """Проверю что при создании поста в одной группе, он не появится в другой группе"""
    def test_group_has_true_posts(self):
        self.group_1 = Group.objects.create(title="TestGroup_1", slug="TestGroup_1", description="Group description_1")
        Post.objects.create(text="Text for new group", author=self.user, group=self.group_1)
        self.post_1 = Post.objects.get(text="Text for new group")
        response = self.guest_client.get(reverse("group", kwargs={"slug": self.group_1.slug}))
        task_text_0 = response.context.get("page")[0].text
        self.assertNotEqual(task_text_0, "This is text")

    """Проверю содержимое словаря context для некоторых страниц"""
    def test_user_page_show_correct_context(self):
        response = self.guest_client.get(reverse("profile", kwargs={"username": "Vera"}))
        self.assertEqual(response.context.get("page")[0].text, "This is text")
        self.assertEqual(response.context.get("author").username, "Vera")

    def test_post_page_show_correct_context(self):
        response = self.guest_client.get(reverse("post", kwargs={"username": "Vera", "post_id": 1}))
        self.assertEqual(response.context.get("post").text, "This is text")

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_client.get(reverse("post_edit", kwargs={"username": "Vera", "post_id": 1}))
        form_field = response.context.get("form").fields.get("text")
        post = response.context.get("post").text
        self.assertIsInstance(form_field, forms.fields.CharField)
        self.assertEqual(post, "This is text")

    """Проверим работу паджинатора. Постов на странице должно быть не больше определенного количества"""
    def test_paginator(self):
        text_list = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "t", "y", "u"]
        for i in range(12):
            Post.objects.create(text=text_list[i], author=self.user, group=self.group)
        response = self.guest_client.get(reverse("index"))
        count = len(response.context.get("page"))
        self.assertEqual(count, 10)


class ImageInPost(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username="Vera")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b')
        cls.group = Group.objects.create(title="TestGroup", slug="TestGroup", description="Group description")
        Post.objects.create(text="This is text", author=cls.user, group=cls.group,
                            image=SimpleUploadedFile(name='small.gif', content=cls.small_gif, content_type='image/gif'))
        cls.post = Post.objects.get(text="This is text")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Рекурсивно удаляем временную после завершения тестов
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    """Проверю что картинка передается на страницу просмотра поста"""
    def test_post_page_show_image(self):
        response = self.guest_client.get(reverse("post", kwargs={"username": "Vera", "post_id": 1}))
        self.assertEqual(response.context.get("page")[0].image, self.post.image)

    """Проверю что картинка передается на главную страницу, страницу профайла и группы"""
    def test_index_page_show_image(self):
        response = self.guest_client.get(reverse("index"))
        task_image = response.context.get("page")[0].image
        self.assertEqual(task_image, self.post.image)

    def test_group_page_show_image(self):
        response = self.guest_client.get(reverse("group", kwargs={"slug": self.group.slug}))
        task_image = response.context.get("page")[0].image
        self.assertEqual(task_image, self.post.image)

    def test_profile_page_show_image(self):
        response = self.guest_client.get(reverse("profile", kwargs={"username": "Vera"}))
        task_image = response.context.get("page")[0].image
        self.assertEqual(task_image, self.post.image)
