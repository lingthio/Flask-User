import pytest


@pytest.fixture
def user_manager():
    from flask_user.user_manager__utils import UserManager__Utils
    return UserManager__Utils()


def test_no_qs(user_manager):
    url = 'https://google.com/'
    safe_url = user_manager.make_safe_url(url)
    assert '/' == safe_url


def test_w_qs(user_manager):
    url = 'https://google.com/search?q=testing'
    safe_url = user_manager.make_safe_url(url)
    assert '/search?q=testing' == safe_url


def test_wo_host_scheme(user_manager):
    url = '/search?q=testing&safe=on'
    safe_url = user_manager.make_safe_url(url)
    assert '/search?q=testing&safe=on' == safe_url


def test_fragment_wo_host(user_manager):
    url = '/search?q=testing&safe=on#row=4'
    safe_url = user_manager.make_safe_url(url)
    assert url == safe_url


def test_qs_and_fragment(user_manager):
    url = 'https://google.com:443/search?q=testing&safe=on#row=4'
    safe_url = user_manager.make_safe_url(url)
    index = url.find('/search')
    assert url[index:] == safe_url
