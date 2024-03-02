# test_routes.py
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, note, expected_status
):
    url = reverse(name, args=(note.slug,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status 


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', pytest.lazy_fixture('slug_for_args')),
        ('notes:edit', pytest.lazy_fixture('slug_for_args')),
        ('notes:delete', pytest.lazy_fixture('slug_for_args')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)




# from http import HTTPStatus

# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse

# from notes.models import Note

# User = get_user_model()


# class TestRoutes(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='Лев Толстой')
#         cls.author_client = Client()
#         cls.author_client.force_login(cls.author)
#         cls.reader = User.objects.create(username='Читатель простой')
#         cls.reader_client = Client()
#         cls.reader_client.force_login(cls.reader)
#         cls.note = Note.objects.create(
#             title='Заголовок',
#             text='Текст',
#             slug='note-slug',
#             author=cls.author,
#         )

#     def test_pages_availability_for_anonymous_user(self):
#         urls = (
#             'notes:home',
#             'users:login',
#             'users:logout',
#             'users:signup',
#         )
#         for page in urls:
#             with self.subTest(page=page):
#                 url = reverse(page)
#                 response = self.client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_pages_availability_for_auth_user(self):
#         urls = (
#             'notes:list',
#             'notes:success',
#             'notes:add',
#         )
#         for page in urls:
#             with self.subTest(page=page):
#                 url = reverse(page)
#                 response = self.author_client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_availability_for_notes_create_edit_and_delete(self):
#         users_statuses = (
#             (self.author_client, HTTPStatus.OK),
#             (self.reader_client, HTTPStatus.NOT_FOUND),
#         )
#         for user, status in users_statuses:
#             for page in ('notes:detail', 'notes:edit', 'notes:delete'):
#                 with self.subTest(user=user, page=page):
#                     url = reverse(page, args=[self.note.slug])
#                     response = user.get(url)
#                     self.assertEqual(response.status_code, status)

#     def test_redirect_for_anonymous_client(self):
#         login_url = reverse('users:login')
#         urls = (
#             ('notes:list', None),
#             ('notes:success', None),
#             ('notes:add', None),
#             ('notes:detail', (self.note.slug,)),
#             ('notes:edit', (self.note.slug,)),
#             ('notes:delete', (self.note.slug,)),
#         )
#         for page, args in urls:
#             with self.subTest(page=page):
#                 url = reverse(page, args=args)
#                 redirect_url = f'{login_url}?next={url}'
#                 response = self.client.get(url)
#                 self.assertRedirects(response, redirect_url)


#НЕ РАБОТАЕТ
# import unittest
# from http import HTTPStatus
# from django.urls import reverse
# from django.test import Client
# from django.test import TestCase

# class TestPagesAvailability(TestCase):
#     @classmethod
#     def setUp(cls):
#         cls.author = User.objects.create(username='')
#         cls.author_client = Client()
#         cls.author_client.force_login(cls.author)
#         cls.reader = User.objects.create(username='')
#         cls.reader_client = Client()
#         cls.reader_client.force_login(cls.reader)
#         cls.note = Note.objects.create(
#             title='Заголовок',
#             text='Текст',
#             slug='note-slug',
#             author=cls.author,
#         )


#     def test_pages_availability_for_anon(self):
#         urls = (
#             'notes:home',
#             'users:login',
#             'users:logout',
#             'users:signup',
#         )
#         for page in urls:
#             with self.subTest(page=page):
#                 url = reverse(page)
#                 response = self.client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)


#     def test_pages_availability_for_user(self):
#         urls = (
#                 'notes:list',
#                 'users:access',
#                 'users:page',
#             )
#         for page in urls:
#             with self.subTest(page=page):
#                 url = reverse(page)
#                 response = self.auth_client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)


#     def test_availability_edit_delete_notes(self):
#         users_statuses = (
#                 (self.author_client, HTTPStatus.OK),
#                 (self.reader_client, HTTPStatus.NOT_FOUND),
#             )
#         for user, status in users_statuses:
#                 for page in ('notes:detail', 'notes:edit', 'notes:delete'):
#                     with self.subTest(user=user, page=page):
#                         url = reverse(page, args=[self.note.slug])
#                         response = user.get(url)
#                         self.assertEqual(response.status_code, status)

#     def test_redirects(self):
#         login_url = reverse('users:login')
#         urls = (
#             ('notes:list', None),
#             ('notes:success', None),
#             ('notes:add', None),
#             ('notes:detail', (self.note.slug,)),
#             ('notes:edit', (self.note.slug,)),
#             ('notes:delete', (self.note.slug,)),
#         )
#         for page, args in urls:
#             with self.subTest(page=page):
#                 url = reverse(page, args=args)
#                 redirect_url = f'{login_url}?next={url}'
#                 response = self.client.get(url)
#                 self.assertRedirects(response, redirect_url)
    
