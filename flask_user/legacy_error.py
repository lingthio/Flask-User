"""This module implements mock Flask-User v0.6 classes
to warn the developer that they are using v0.6 API calls
against an incompatible v1.0+ Flask-User install.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

LEGACY_ERROR =\
"""
Flask-User Legacy ERROR:
-----------------------------------
You are trying to use the Flask-User v0.6 API
against an _incompatible_ Flask-User v1.0 install.

Flask-User v1.0:
- Is in its _Alpha_ stage, and not ready for production,
- Is no longer compatible with v0.6,
- Has no changes in the way it customizes form and email templates.
- Has a few changes in its configuration settings,
- Has completely changed the way you customize form classes and views,
- Has completely changed the way you customize passwords and tokens.

1) Please downgrade Flask-User back to the latest v0.6 version, or
2) read https://flask-user.readthedocs.io/en/latest/porting.html

To downgrade Flask-User:
- Install the latest v0.6 Flask-User
      pip install "Flask-User<0.7"
- Make note of the latest Flask-v0.6 version (Flask-User==0.6.{X})
      pip freeze | grep Flask-User
- Update your requirements.txt file to pin the Flask-User version
      Flask-User==0.6.{X}
"""

class DbAdapter(object):
    """This is mock Flask-User v0.6 class
    to warn the developer that they are using v0.6 API calls
    against an incompatible v1.0+ Flask-User install.
    """

    def __init__(self, db, UserClass, UserAuthClass=None, UserEmailClass=None, UserProfileClass=None, UserInvitationClass=None):
        raise Exception(LEGACY_ERROR)

class SQLAlchemyAdapter(DbAdapter):
    """This is mock Flask-User v0.6 class
    to warn the developer that they are using v0.6 API calls
    against an incompatible v1.0+ Flask-User install.
    """
    def __init__(self, db, UserClass, UserProfileClass=None, UserAuthClass=None, UserEmailClass=None, UserInvitationClass=None):
        raise Exception(LEGACY_ERROR)

