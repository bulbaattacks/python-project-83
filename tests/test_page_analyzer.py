import pytest
from page_analyzer.app import app


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


def test_add_url_wrong_data(client):
    response = client.post('/urls', data={"url": "wrong_data"}, follow_redirects=True)
    assert response.status_code == 422
