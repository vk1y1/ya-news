"""Фикстуры для тестов pytest_tests."""
from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from news.forms import BAD_WORDS
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    """Создаёт объект автор."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    """Создаёт объект читатель."""
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    """Создаёт авторизованного клиента автора."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    """Создаёт авторизованного клиента читателя."""
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    """Возвращает объект новости."""
    return News.objects.create(
        title='Заголовок новости',
        text='Текст новости',
    )


@pytest.fixture
def comment(news, author):
    """Возвращает объект комментария."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def form_data():
    """Возвращает текст для комментария."""
    return {'text': 'Текст комментария'}


@pytest.fixture
def new_form_data():
    """Возвращает текст для комментария."""
    return {'text': 'Обновлённый комментарий'}


@pytest.fixture
def bad_words_data():
    """Возвращает текст для комментария с запрещёнными словами."""
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


@pytest.fixture
def id_for_news(news):
    """Возвращает id новости."""
    return (news.id,)


@pytest.fixture
def id_for_comment(comment):
    """Возвращает id комментария."""
    return (comment.id,)


@pytest.fixture
def login_url():
    """Возвращает адрес страницы авторизации."""
    return reverse('users:login')


@pytest.fixture
def home_url():
    """Возвращает адрес домашней страницы."""
    return reverse('news:home')


@pytest.fixture
def detail_url(id_for_news):
    """Возвращает адрес отдельной новости."""
    return reverse('news:detail', args=id_for_news)


@pytest.fixture
def url_to_comments(detail_url):
    """Возвращает адрес отдельной новости с комментариями."""
    return detail_url + '#comments'


@pytest.fixture
def edit_url(id_for_comment):
    """Возвращает адрес для редактирования комментария."""
    return reverse('news:edit', args=id_for_comment)


@pytest.fixture
def delete_url(id_for_comment):
    """Возвращает адрес для удаления комментария."""
    return reverse('news:delete', args=id_for_comment)


@pytest.fixture
def today_date():
    """Возвращает текущую дату."""
    return datetime.today()


@pytest.fixture
def several_news(today_date):
    """Создаёт несколько объектов новостей."""
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today_date - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def today_date_time():
    """Возвращает текущее время в часовом поясе по умолчанию приложения."""
    return timezone.now()


@pytest.fixture
def several_comments(news, author, today_date_time):
    """Создаёт несколько объектов комментариев."""
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = today_date_time + timedelta(days=index)
        comment.save()


@pytest.fixture
def http_status_found():
    """Возвращает статус код 302."""
    return HTTPStatus.FOUND


@pytest.fixture
def http_status_not_found():
    """Возвращает статус код 404."""
    return HTTPStatus.NOT_FOUND


@pytest.fixture
def http_status_ok():
    """Возвращает статус код 200."""
    return HTTPStatus.OK


@pytest.fixture
def zero_comment():
    """Возвращает число 0."""
    return 0


@pytest.fixture
def one_comment():
    """Возвращает число 1."""
    return 1
