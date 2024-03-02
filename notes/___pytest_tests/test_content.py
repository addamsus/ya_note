# test_content.py
import pytest

from django.urls import reverse
from notes.forms import NoteForm


@pytest.mark.parametrize(
    'parametrized_client, note_in_list',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), False),
    )
)
def test_notes_list_for_different_users(
        note, parametrized_client, note_in_list
):
    url = reverse('notes:list')
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    assert (note in object_list) is note_in_list


def test_create_note_page_contains_form(author_client):
    url = reverse('notes:add')
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], NoteForm)


def test_edit_note_page_contains_form(slug_for_args, author_client):
    url = reverse('notes:edit', args=slug_for_args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], NoteForm)

@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:add', None),
        ('notes:edit', pytest.lazy_fixture('slug_for_args'))
    )
)
def test_pages_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], NoteForm)




# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse

# from notes.models import Note
# from notes.forms import NoteForm

# User = get_user_model()


# class TestContent(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='Автор Петрович')
#         cls.author_client = Client()
#         cls.author_client.force_login(cls.author)
#         cls.reader = User.objects.create(username='Читатель Иванович')
#         cls.reader_client = Client()
#         cls.reader_client.force_login(cls.reader)
#         cls.note = Note.objects.create(
#             title='Заголовок',
#             text='Текст',
#             slug='note-slug',
#             author=cls.author,
#         )

#     def test_notes_list_for_different_users(self):
#         users = (
#             (self.author_client, True),
#             (self.reader_client, False),
#         )
#         url = reverse('notes:list')
#         for user, value in users:
#             with self.subTest(user=user):
#                 object_list = user.get(url).context['object_list']
#                 self.assertTrue((self.note in object_list) is value)

#     def test_pages_contains_form(self):
#         urls = (
#             ('notes:add', None),
#             ('notes:edit', (self.note.slug,)),
#         )
#         for page, args in urls:
#             with self.subTest(page=page):
#                 url = reverse(page, args=args)
#                 response = self.author_client.get(url)
#                 assert ('form' in response.context)
#                 self.assertIsInstance(response.context['form'], NoteForm)



#НЕ РАБОТАЕТ
# import unittest
# import pytest
# from django.urls import reverse

# class TestNotesListForDifferentUsers(unittest.TestCase):
#     @pytest.mark.parametrize(
#     'parametrized_client, note_in_list',
#     (
#         (pytest.lazy_fixture('author_client'), True),
#         (pytest.lazy_fixture('not_author_client'), False),
#     )
# )
#     def test_notes_list_for_different_users(self, note, parametrized_client, note_in_list):
#         url = reverse('notes:list')
#         response = parametrized_client.get(url)
#         object_list = response.context['object_list']
#         self.assertEqual((note in object_list), note_in_list)

# class TestCreateNotePageContainsForm(unittest.TestCase):
#     def test_create_note_page_contains_form(self, author_client):
#         url = reverse('notes:add')
#         response = author_client.get(url)
#         self.assertTrue('form' in response.context)
#         self.assertIsInstance(response.context['form'], NoteForm)

# class TestEditNotePageContainsForm(unittest.TestCase):
#     def test_edit_note_page_contains_form(self, slug_for_args, author_client):
#         url = reverse('notes:edit', args=slug_for_args)
#         response = author_client.get(url)
#         self.assertTrue('form' in response.context)
#         self.assertIsInstance(response.context['form'], NoteForm)

# class TestPagesContainsForm(unittest.TestCase):
#     @pytest.mark.parametrize(
#     'name, args',
#     (
#         ('notes:add', None),
#         ('notes:edit', pytest.lazy_fixture('slug_for_args'))
#     )
# )
#     def test_pages_contains_form(self, author_client, name, args):
#         url = reverse(name, args=args)
#         response = author_client.get(url)
#         self.assertTrue('form' in response.context)
#         self.assertIsInstance(response.context['form'], NoteForm)

