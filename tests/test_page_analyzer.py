import pytest
from page_analyzer.app import app
from bs4 import BeautifulSoup


@pytest.fixture()
def test_app_create():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    yield test_app


@pytest.fixture()
def client(test_app_create):
    return test_app_create.test_client()




def test_index(client):
    response = client.get('/')
    html = response.data.decode()
    assert response.status_code == 200
    assert '<h1 class="display-3">Анализатор страниц</h1>' in html
    assert '<p class="lead">Бесплатно проверяйте сайты на SEO пригодность</p>' in html


def test_get_urls(client):
    response = client.get('/urls')
    html = response.data.decode()
    assert response.status_code == 200
    assert '<h1>Сайты</h1>' in html
    assert '<th>ID</th>' in html
    assert '<th>Имя</th>' in html
    assert '<th>Последняя проверка</th>' in html
    assert '<th>Код ответа</th>' in html


def test_add_url(client):
    response = client.post('/urls', data={"url": "https://mail.ru"})
    assert response.status_code == 302


def test_add_url_redirect(client):
    response = client.post('/urls', data={"url": "https://mail.ru"}, follow_redirects=True)
    assert len(response.history) == 1
    assert response.status_code == 200
    html = response.data.decode()
    assert '<h2 class="mt-5 mb-3">Проверки</h2>' in html


def test_add_url_wrong_data(client):
    response = client.post('/urls', data={"url": "wrong_data"}, follow_redirects=True)
    assert response.status_code == 422


def test_page_not_found(client):
    response = client.get('/urls/190000000000000000000003338338833888322222')
    assert response.status_code == 404


def test_show_url(client):
    response = client.post('/urls', data={"url": "https://mail.ru"}, follow_redirects=True)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.h1.text
    assert 'https://mail.ru' in h1


