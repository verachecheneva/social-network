from django.test import Client, TestCase

from posts.models import Post, Group, User


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username="Vera")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(title="TestGroup", slug="TestGroup",description="Group description")
        Post.objects.create(text="This is text", author=cls.user, group=cls.group)
        cls.post = Post.objects.get(text="This is text")
        cls.user_1 = User.objects.create_user(username="Alina")
        cls.other_client = Client()
        cls.other_client.force_login(cls.user_1)

    """Тесты на доступность страниц"""
    def test_homepage_for_everyone(self):
        response = self.guest_client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_GroupPage_for_everyone(self):
        response = self.guest_client.get("/group/TestGroup/")
        self.assertEqual(response.status_code, 200)

    def test_UserPage_for_everyone(self):
        response = self.guest_client.get("/Vera/")
        self.assertEqual(response.status_code, 200)

    def test_PostPage_for_everyone(self):
        response = self.guest_client.get("/Vera/1/")
        self.assertEqual(response.status_code, 200)

    def test_NewPost_for_anonymous(self):
        response = self.guest_client.get("/new/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/")

    def test_NewPost_for_users(self):
        response = self.authorized_client.get("/new/")
        self.assertEqual(response.status_code, 200)

    def test_EditPost_for_anonymous(self):
        response = self.guest_client.get("/Vera/1/edit/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/Vera/1/edit/")

    def test_EditPost_for_user_not_author(self):
        response = self.other_client.get("/Vera/1/edit/", follow=True)
        self.assertRedirects(response, "/Vera/1/")

    def test_EditPost_for_user_author(self):
        response = self.authorized_client.get("/Vera/1/edit/", follow=True)
        self.assertEqual(response.status_code, 200)

        """Тесты на ожидаемые шаблоны"""
    def test_urls_uses_correct_templates(self):
        templates_url_names = {
            "index.html": "/",
            "group.html": "/group/TestGroup/",
            "new_post.html": "/new/",
            "new_post.html": "/Vera/1/edit/"
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
