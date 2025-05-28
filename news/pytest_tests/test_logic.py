"""Тестирование логики проекта YaNews."""

import pytest
from news.forms import WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client, detail_url, form_data, zero_comment):
    """Проверяет невозможность отправки комментария анонимным пользователем."""
    client.post(detail_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == zero_comment


def test_user_can_create_comment(
        reader, reader_client, news, detail_url, form_data):
    """Проверяет может ли отправить комментария авторизованный пользователь."""
    response = reader_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == reader


def test_user_cant_use_bad_words(
        reader_client, detail_url, bad_words_data, zero_comment):
    """Проверяет на невозможноть публикации с запрещёнными словами."""
    response = reader_client.post(detail_url, data=bad_words_data)
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == zero_comment


def test_author_can_delete_comment(
        author_client,
        news,
        comment,
        delete_url,
        url_to_comments,
        http_status_found,
        zero_comment
):
    """Проверяет возможность удалять комментарий автором."""
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert response.status_code == http_status_found
    comments_count = Comment.objects.count()
    assert comments_count == zero_comment


def test_user_cant_delete_comment_of_another_user(
        reader_client,
        news,
        comment,
        delete_url,
        url_to_comments,
        http_status_not_found,
        one_comment
):
    """Проверяет невозможность удалять чужой комментарий читателем."""
    response = reader_client.delete(delete_url)
    assert response.status_code == http_status_not_found
    comments_count = Comment.objects.count()
    assert comments_count == one_comment


def test_author_can_edit_comment(
        author_client,
        news,
        comment,
        edit_url,
        new_form_data,
        url_to_comments
):
    """Проверяет возможность редактировать комментарий автором."""
    response = author_client.post(edit_url, data=new_form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text, new_form_data['text']


def test_user_cant_edit_comment_of_another_user(
        reader_client,
        news,
        comment,
        edit_url,
        form_data,
        new_form_data,
        http_status_not_found
):
    """Проверяет невозможность редактировать чужой комментарий читателем."""
    response = reader_client.post(edit_url, data=new_form_data)
    assert response.status_code == http_status_not_found
    comment.refresh_from_db()
    assert comment.text == form_data['text']
