# from django.test import TestCase
# from django.contrib.auth import get_user_model
#
# from posts.models import Post, Group
#
#
# class PostModelTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         user = get_user_model().objects.create_user(username="Vera")
#         Post.objects.create(text="This is text", author=user.username, group="group")
#         cls.post = Post.objects.get(text="This is text")
#
#     def test_text_label(self):
#         post = PostModelTest.post
#         verbose = post._meta.get_field("text").verbose_name
#         self.assertEquals(verbose, "Текст поста")
#
#     def test_text_help_text(self):
#         post = PostModelTest.post
#         help_texts = post._meta.get_field("text").help_text
#         self.assertEquals(help_texts, "Введите текст поста")
#
#     def test_group_label(self):
#         post = PostModelTest.post
#         verbose = post._meta.get_field("group").verbose_name
#         self.assertEquals(verbose, "Группа")
#
#     def test_group_help_text(self):
#         post = PostModelTest.post
#         help_texts = post._meta.get_field("group").help_text
#         self.assertEquals(help_texts, "Выберите группу")
#
#     def test_objects_some_posts(self):
#         post = PostModelTest.post
#         expected_posts = post.text[:15]
#         self.assertEquals(expected_posts, str(post))
#
#
# class GroupModelTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         Group.objects.create(title="GroupName", slug="GroupName", description="Little Group")
#         cls.group = Group.objects.get(slug="GroupName")
#
#     def test_objects_str_func(self):
#         group = GroupModelTest.group
#         expected_objects = group.title
#         self.assertEquals(expected_objects, str(group))
