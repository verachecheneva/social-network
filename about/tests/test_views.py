from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_AboutAuthorPage_uses_correct_template(self):
        response = self.guest_client.get(reverse("about:author"))
        self.assertTemplateUsed(response, "AboutAuthor.html")

    def test_AboutTechPage_uses_correct_template(self):
        response = self.guest_client.get(reverse("about:tech"))
        self.assertTemplateUsed(response, "AboutTech.html")
