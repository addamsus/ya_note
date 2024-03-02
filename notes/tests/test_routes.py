import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', author=cls.author)
        cls.reader = User.objects.create(username='Читатель простой')

        cls.anon_client = Client()

        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

    def test_index_page_availability(self):
        response = self.anon_client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK) 

    def test_reader_pages_availability(self):
        response = self.reader_client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.reader_client.get(reverse('notes:success'))
        self.assertEqual(response.status_code, HTTPStatus.OK) 

        response = self.reader_client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, HTTPStatus.OK) 

    def test_author_pages_availability(self):
        response = self.author_client.get(reverse('notes:detail', kwargs={'slug': self.note.slug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.reader_client.get(reverse('notes:detail', kwargs={'slug': self.note.slug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.author_client.get(reverse('notes:edit', kwargs={'slug': self.note.slug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.reader_client.get(reverse('notes:edit', kwargs={'slug': self.note.slug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.author_client.get(reverse('notes:delete', kwargs={'slug': self.note.slug}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.reader_client.get(reverse('notes:delete', kwargs={'slug': self.note.slug}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_for_anonymous_client_common(self):
        login_url = reverse('users:login')

        for name in ('add', 'list', 'success'):
            with self.subTest(name=name):
                url = reverse(f'notes:{name}')

                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')

        for name in ('edit', 'detail', 'delete'):
            with self.subTest(name=name):
                url = reverse(f'notes:{name}', kwargs={'slug': self.note.slug})

                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url) 

    def test_auth_pages_availability(self):
        for name in ('users:login', 'users:logout', 'users:signup'):
            with self.subTest(name=name):
                response = self.anon_client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK) 
