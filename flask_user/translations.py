""" This module contains functions to translate strings for Flask-User.
    The functions are based on Flask-Babel.

    It redefines flask_babel.get_translations() to change the following:
    - look for translations first in the app.root_dir, then in the flask_user dir
    - change the domain from 'messages' to 'flask_user'

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

import os
import gettext as python_gettext

from flask import _request_ctx_stack, current_app, render_template
from flask.ext.babel import get_locale, support

def get_translations():
    """ Search the Application directory and the Flask-User directory for the
        Flask-User translations file and return a Translations() object."""
    ctx = _request_ctx_stack.top
    if ctx is None:
        return None
    translations = getattr(ctx, 'flask_user_translations', None)
    if translations is None:
        # Prepare settings
        domain = 'flask_user'
        locales = [get_locale()]
        languages = [str(locale) for locale in locales]
        # Search Application directory
        app_dir = os.path.join(current_app.root_path, 'translations')
        filename = python_gettext.find(domain, app_dir, languages)
        if filename:
            translations = support.Translations.load(app_dir, locales, domain=domain)
        else:
            # Search Flask-User directory
            flask_user_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translations')
            translations = support.Translations.load(flask_user_dir, locales, domain=domain)

        ctx.flask_user_translations = translations

    return ctx.flask_user_translations

def gettext(string, **variables):
    """ Translate specified string."""
    translations = get_translations()
    if not translations:
        return string % variables
    return translations.ugettext(string) % variables

def ngettext(singular, plural, num, **variables):
    """ Translate a singular/plural string based on the number 'num'."""
    translations = get_translations()
    variables.setdefault('num', num)
    if not translations:
        return (singular if num == 1 else plural) % variables
    return translations.ungettext(singular, plural, num) % variables

def lazy_gettext(string, **variables):
    """ Similar to 'gettext' but the string returned is lazy which means
        it will be translated when it is used as an actual string."""
    from speaklater import make_lazy_string
    return make_lazy_string(gettext, string, **variables)

_ = lazy_gettext
_home_page = _('Home Page')
_profile_page = _('Profile Page')
_special_page = _('Special Page')
