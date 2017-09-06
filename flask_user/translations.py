""" This file contains functions to translate strings for Flask-User.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.

import os
from flask import _request_ctx_stack, request

# Return absolute path to Flask-User's translations dir ('/full/path/to/flask_user/translations')
def get_flask_user_translations_dir():
    translations_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translations')
    return translations_dir

# Chooses the best locale from a list of available locales
def choose_best_locale(app, babel, flask_user_translations_dir):
    # babel.list_translations() does not accept a custom translations directory
    # As a workaround, we:
    # - temporarily set BABEL_TRANSLATION_DIRECTORIES=flask_user_translations_dir
    # - call babel.list_translations()
    # - restore BABEL_TRANSLATION_DIRECTORIES

    # set BABEL_TRANSLATION_DIRECTORIES=flask_user_translations_dir
    original_dir = app.config.get('BABEL_TRANSLATION_DIRECTORIES', '')
    app.config.update(BABEL_TRANSLATION_DIRECTORIES=flask_user_translations_dir)

    # Retrieve a list of available translation codes from Flask-User. E.g. ['de', 'en', 'fr']
    available_codes = [str(translation) for translation in babel.list_translations()]

    # Restore BABEL_TRANSLATION_DIRECTORIES
    app.config.update(BABEL_TRANSLATION_DIRECTORIES=original_dir)

    # Match list with languages from the user's browser's accept header
    locale = request.accept_languages.best_match(available_codes)

    return locale


# To avoid requiring the Flask-Babel, Babel and speaklater packages,
# we check if the app has initialized Flask-Babel or not
def get_translations():
    # If there is no request context: return None
    ctx = _request_ctx_stack.top
    if ctx is None: return None
    app = ctx.app

    # If babel is not setup: return None
    babel = app.extensions.get('babel', None)
    if babel is None: return None

    # Only load translations if it has not yet been loaded before
    translations = getattr(ctx, 'flask_user_translations', None)
    if translations is None:
        from flask_babel import support
        flask_user_translations_dir = get_flask_user_translations_dir()
        # Chooses the best locale from a list of available locales
        locale = choose_best_locale(app, babel, flask_user_translations_dir)
        locales = [locale]

        # Load translations from dir/<locales>/LC_MESSAGES/<domain>.mo
        translations = support.Translations.load(flask_user_translations_dir, locales, domain='flask_user')
        ctx.flask_user_translations = translations

    return translations

def gettext(string, **variables):
    """ Translate specified string."""
    translations = get_translations()
    if translations:
        return translations.ugettext(string) % variables
    return string % variables    # pragma: no cover

# def ngettext(singular, plural, num, **variables):
#     """ Translate a singular/plural string based on the number 'num'."""
#     translations = get_translations()
#     variables.setdefault('num', num)
#     if translations:
#         return translations.ungettext(singular, plural, num) % variables
#     return (singular if num == 1 else plural) % variables

def lazy_gettext(string, **variables):
    """ Similar to 'gettext' but the string returned is lazy which means
        it will be translated when it is used as an actual string."""
    try:
        from speaklater import make_lazy_string
        return make_lazy_string(gettext, string, **variables)
    except ImportError:
       return string % variables

_ = lazy_gettext
_home_page = _('Home Page')
_profile_page = _('Profile Page')
_special_page = _('Special Page')
