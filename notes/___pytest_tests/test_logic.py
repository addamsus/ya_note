# test_logic.py
from pytest_django.asserts import assertRedirects
from pytest_django.asserts import assertRedirects, assertFormError
import pytest
from pytils.translit import slugify
from django.urls import reverse
from http import HTTPStatus

from notes.models import Note
from notes.forms import WARNING

# import unittest
# User = get_user_model()

def test_user_can_create_note(author_client, author, form_data):
    url = reverse('notes:add')
    response = author_client.post(url, data=form_data)
    assertRedirects(response, reverse('notes:success'))
    assert Note.objects.count() == 1
    new_note = Note.objects.get()
    assert new_note.title == form_data['title']
    assert new_note.text == form_data['text']
    assert new_note.slug == form_data['slug']
    assert new_note.author == author

@pytest.mark.django_db
def test_anonymous_user_cant_create_note(client, form_data):
    url = reverse('notes:add')
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Note.objects.count() == 0

def test_not_unique_slug(author_client, note, form_data):
    url = reverse('notes:add')
    form_data['slug'] = note.slug
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'slug', errors=(note.slug + WARNING))
    assert Note.objects.count() == 1

def test_empty_slug(author_client, form_data):
    url = reverse('notes:add')
    form_data.pop('slug')
    response = author_client.post(url, data=form_data)
    assertRedirects(response, reverse('notes:success'))
    assert Note.objects.count() == 1
    new_note = Note.objects.get()
    expected_slug = slugify(form_data['title'])
    assert new_note.slug == expected_slug

def test_author_can_edit_note(author_client, form_data, note):
    url = reverse('notes:edit', args=(note.slug,))
    response = author_client.post(url, form_data)
    assertRedirects(response, reverse('notes:success'))
    note.refresh_from_db()
    assert note.title == form_data['title']
    assert note.text == form_data['text']
    assert note.slug == form_data['slug']

def test_other_user_cant_edit_note(not_author_client, form_data, note):
    url = reverse('notes:edit', args=(note.slug,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Note.objects.get(id=note.id)
    assert note.title == note_from_db.title
    assert note.text == note_from_db.text
    assert note.slug == note_from_db.slug

def test_author_can_delete_note(author_client, slug_for_args):
    url = reverse('notes:delete', args=slug_for_args)
    response = author_client.post(url)
    assertRedirects(response, reverse('notes:success'))
    assert Note.objects.count() == 0


def test_other_user_cant_delete_note(not_author_client, form_data, slug_for_args):
    url = reverse('notes:delete', args=slug_for_args)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Note.objects.count() == 1


# class TestLogic(unittest.TestCase):
#     NOTE_TEXT='Текст заметки'
#     NOTE_TITLE='Заголовок заметки'
#     URL_NOTE=url = reverse('notes:add')


#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(usernme='Имя Фамилия')
#         cls.url = reverse('news:detail', args=(cls.news.id,))
#         cls.auth_client = Client()
#         cls.user_client.force_login(cls.user)
#         cls.form_data = {'title': cls.NOTE_TITLE,
#                          'text':cls.NOTE_TEXT,
#                          'slug':,
#                          }


#     def test_anonymous_user_cant_create_note(self):    
#         self.client.note(self.url, data=self.form_data)
#         notes_count = Note.objects.count()
#         self.assertEqual(notes_count, 0)
    
#     def test_user_can_create_note(self):
#         response = self.auth_client.post(self.url, data=self.form_data)
#         self.assertRedirects(response, f'{self.url}#notes')
#         notes_count = Note.objects.count()
#         self.assertEqual(notes_count, 1)
#         note = Note.objects.get()
#         self.assertEqual(note.text, self.COMMENT_TEXT)
#         self.assertEqual(note.notes, self.notes)
#         self.assertEqual(note.author, self.user)
    
#     def test_not_unique_slug(self):
    

    # def test_empty_slug(self)