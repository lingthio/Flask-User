from flask import url_for

# Logs a user in using POST /account/login
def login(client, username='', email='', password='Password1'):
    url = url_for('user.login')
    response = client.post(url, data=dict(
        username=username,
        email=email,
        password=password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert response_has_no_errors(response)

# Logs a user out using GET /account/logout
def logout(client):
    url = url_for('user.logout')
    response = client.get(url, follow_redirects=True)
    assert response.status_code == 200

# Checks to see if response.data contains no 'has-error' strings
def response_has_no_errors(response):
    return not response_has_errors(response)

# Checks to see if response.data contains the string 'has-error'.
def response_has_errors(response):
    return response_has_string(response, 'has-error')

# Checks to see if response.data contains the specified string.
def response_has_string(response, string):
    assert response.status_code == 200
    return response.data.find(string) >= 0
