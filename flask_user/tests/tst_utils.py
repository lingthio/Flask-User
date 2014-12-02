"""
    tests.utils
    -----------
    Utility class for Flask-User automated tests

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""
from __future__ import print_function
from flask import url_for

# Checks to see if response.data contains the specified string.
def response_has_string(response, string):
    assert response.status_code == 200
    # In Python3, response.data is <class 'bytes'> and string is <class 'str'>
    # hence the use of 'str.encode(string)'
    return response.data.find(str.encode(string)) >= 0

# Checks to see if response.data contains the string 'has-error'.
def response_has_errors(response):
    return response_has_string(response, 'has-error') or response_has_string(response, 'alert-danger')

# Checks to see if response.data contains no 'has-error' strings
def response_has_no_errors(response):
    has_errors = response_has_errors(response)
    if has_errors:
        print(response.data)
    return not has_errors

class TstClient(object):
    """
    Utility class for tests
    """
    def __init__(self, client, db):
        self.client = client
        self.db = db

    def get_valid_page(self, url):
        """
        GET url and assert that the response contains no errors.
        """
        response = self.client.get(url, follow_redirects=True)
        assert response.status_code == 200, "GET %s returned %d" % (url, response.status_code)
        assert response_has_no_errors(response), "GET %s returned an error" % url
        return response

    def get_invalid_page(self, url, expected_error):
        """
        GET url and assert that the response contains an expected error.
        """
        response = self.client.get(url, follow_redirects=True)
        assert response.status_code == 200, "POST %s returned %d" % (url, response.status_code)
        response_has_error = response_has_string(response, expected_error)
        if not response_has_error:
            print(response.data)
        assert response_has_error, "POST %s did not contain '%s' error" % (url, expected_error)
        return response

    def post_valid_form(self, url, **kwargs):
        """
        POST url and assert that the response contains no errors.
        """
        response = self.client.post(url, data=kwargs, follow_redirects=True)
        assert response.status_code == 200, "POST %s returned %d" % (url, response.status_code)
        assert response_has_no_errors(response), "post_valid_form(%s) returned an error" % url
        return response

    def post_invalid_form(self, url, expected_error, **kwargs):
        """
        POST url and assert that the response contains an expected error.
        """
        response = self.client.post(url, data=kwargs, follow_redirects=True)
        assert response.status_code == 200, "POST %s returned %d" % (url, response.status_code)
        response_has_error = response_has_string(response, expected_error)
        if not response_has_error:
            print(response.data)
        assert response_has_error, "POST %s did not contain '%s' error" % (url, expected_error)
        return response

    def login(self, **kwargs):
        """
        Log new user in with username/password or email/password.
        """
        url = url_for('user.login')
        return self.post_valid_form(url, **kwargs)

    def logout(self, **kwargs):
        """
        Log current user out.
        """
        url = url_for('user.logout')
        response = self.client.get(url, follow_redirects=True)
        assert response.status_code == 200

