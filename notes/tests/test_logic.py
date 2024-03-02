import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.forms import WARNING, NoteForm
from pytils.translit import slugify

from notes.models import Note
from yanote import settings

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.not_author = User.objects.create(username='Читатель простой')

        cls.anon_client = Client()

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

    def make_form_data(self):
        return {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

    def test_user_can_create_note(self):
        url = reverse('notes:add')
        form_data = self.make_form_data()
        response = self.author_client.post(url, data=form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEquals(Note.objects.count(), 1)
        new_note = Note.objects.get()

        self.assertEquals(new_note.title, form_data['title'])
        self.assertEquals(new_note.text, form_data['text'])
        self.assertEquals(new_note.slug, form_data['slug'])
        self.assertEquals(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        url = reverse('notes:add')
        form_data = self.make_form_data()
        response = self.anon_client.post(url, data=form_data)

        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={url}'
        self.assertRedirects(response, expected_url)
        assert Note.objects.count() == 0

    def test_not_unique_slug(self):
        note = Note.objects.create(title='Заголовок', text='Текст', author=self.author, slug='test_slug')

        url = reverse('notes:add')
        form_data = self.make_form_data()
        form_data['slug'] = 'test_slug'

        response = self.author_client.post(url, data=form_data)
        self.assertFormError(response, 'form', 'slug', errors=(note.slug + WARNING))
        self.assertEquals(Note.objects.count(), 1)

    def test_empty_slug(self):
        url = reverse('notes:add')
        form_data = self.make_form_data()
        form_data.pop('slug')

        response = self.author_client.post(url, data=form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEquals(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(form_data['title'])
        assert new_note.slug == expected_slug

    def test_author_can_edit_note(self):
        form_data = self.make_form_data()
        note = Note.objects.create(title='Заголовок', text='Текст', author=self.author)


        url = reverse('notes:edit', args=(note.slug,))
        response = self.author_client.post(url, form_data)

        self.assertRedirects(response, reverse('notes:success'))
        note.refresh_from_db()

        assert note.title == form_data['title']
        assert note.text == form_data['text']
        assert note.slug == form_data['slug']

    def test_other_user_cant_edit_note(self):
        form_data = self.make_form_data()
        note = Note.objects.create(title='Заголовок', text='Текст', author=self.author)

        url = reverse('notes:edit', args=(note.slug,))
        response = self.not_author_client.post(url, form_data)
        assert response.status_code == HTTPStatus.NOT_FOUND
        note_from_db = Note.objects.get(id=note.id)
        assert note.title == note_from_db.title
        assert note.text == note_from_db.text
        assert note.slug == note_from_db.slug

    def test_author_can_delete_note(self):
        note = Note.objects.create(title='Заголовок', text='Текст', author=self.author, slug="test_slug")

        url = reverse('notes:delete', args=('test_slug', ))
        response = self.author_client.post(url)
        self.assertRedirects(response, reverse('notes:success'))
        assert Note.objects.count() == 0

    def test_other_user_cant_delete_note(self):
        note = Note.objects.create(title='Заголовок', text='Текст', author=self.author, slug="test_slug")

        url = reverse('notes:delete', args=("test_slug", ))
        response = self.not_author_client.post(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert Note.objects.count() == 1
