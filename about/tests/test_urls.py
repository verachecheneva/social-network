from django.test import Client, TestCase


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_AboutAuthor_page(self):
        response = self.guest_client.get("/about/author/")
        self.assertEqual(response.status_code, 200)

    def test_AboutTech_page(self):
        response = self.guest_client.get("/about/tech/")
        self.assertEqual(response.status_code, 200)
