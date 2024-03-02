import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.forms import NoteForm

from notes.models import Note
from yanote import settings

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', author=cls.user1)
        cls.user2 = User.objects.create(username='Читатель простой')

        cls.anon_client = Client()

        cls.client1 = Client()
        cls.client1.force_login(cls.user1)

        cls.client2 = Client()
        cls.client2.force_login(cls.user2)

        for index in range(500):
            Note.objects.create(title=f'Заметка {index}', text='Просто текст.' * index, author=cls.user2) 

    def test_note_in_list(self):
        url = reverse('notes:list')
        response = self.client1.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_separete_note_lists(self):
        url = reverse('notes:list')
        response = self.client2.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_create_note_page_contains_form(self):
        url = reverse('notes:add')
        response = self.client1.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_contains_form(self):
        url = reverse('notes:edit', kwargs={'slug': self.note.slug})
        response = self.client1.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

