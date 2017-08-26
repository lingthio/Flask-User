""" This file shields Flask-User code from database/ORM specific functions.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from __future__ import print_function

class DbAdapter(object):
    """ This class is used to shield Flask-User from database specific calls.
        It is used as the base class for ORM specific adapters like SQLAlchemyDbAdapter."""

    def __init__(self, db):
        self.db = db

    # Optional method for ORMs with db.session.commit() functionality (e.g. SQLAlchemy)
    def commit(self):
        pass