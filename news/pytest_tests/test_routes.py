"""Тестирование маршрутов проекта YaNews."""
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', lf('id_for_news')),
    ),
)
def test_home_availability_for_anonymous_user(
        client, name, args, http_status_ok):
    """Проверяет доступность страниц анонимному пользователю."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == http_status_ok


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('reader_client'), lf('http_status_not_found')),
        (lf('author_client'), lf('http_status_ok'))
    ),
)
@pytest.mark.parametrize(
    'name',
    (lf('edit_url'), lf('delete_url'))
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, name, expected_status
):
    """Проверяет доступность страниц удаления и редактирования комментария."""
    response = parametrized_client.get(name)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        (lf('edit_url')),
        (lf('delete_url'))
    ),
)
def test_redirect_for_anonymous_client(client, name, login_url):
    """Проверяет переадресацию анонима на страницу авторизации."""
    expected_url = f'{login_url}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)
