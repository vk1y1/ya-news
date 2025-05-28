"""Тестирование контента проекта YaNews."""
import pytest
from django.conf import settings
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, home_url, several_news):
    """Проверяет количество новостей на главной странице - не более 10."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, home_url, several_news):
    """Проверяет сортировку новостей на странице - свежие в начале списка."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, several_comments, detail_url):
    """Проверяет сортировку комментариев - старые в начале списка."""
    response = client.get(detail_url)
    assert 'news' in response.context
    response_news = response.context['news']
    all_comments = response_news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news, detail_url):
    """Проверяет недоступность формы комментария анонимному пользователю."""
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news, detail_url):
    """Проверяет доступность формы комментария авторизованному пользователю."""
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
