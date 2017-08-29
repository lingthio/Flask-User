from flask import url_for

login_data = {
    'username': 'member',
    'email': 'member@example.com',
    'password': 'Password1',
}


def test_internal_url(client):
    internal_url = url_for('user_profile_page')
    data = dict(login_data, next=internal_url)
    response = client.client.post(url_for('user.login'), data=data)
    assert response.status_code == 302
    assert response.location == internal_url


def test_external_url(client):
    data = dict(login_data, next='https://example.net')
    response = client.client.post(url_for('user.login', data=data))
    assert response.status_code == 302
    assert response.location == url_for('home_page')
