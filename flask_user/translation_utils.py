""" This module implements utility functions to offer translations.
It uses Flask-BabelEx to manage domain specific translation files.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

import os
from flask import request

_translations_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translations')

# Load Flask-User translations, if Flask-BabelEx has been installed
try:
    from flask_babelex import Domain

    # Retrieve Flask-User translations from the flask_user/translations directory
    domain_translations = Domain(_translations_dir, domain='flask_user')
except ImportError:
    domain_translations = None

def gettext(string, **variables):
    return domain_translations.gettext(string, **variables) if domain_translations else string % variables

def lazy_gettext(string, **variables):
    return domain_translations.lazy_gettext(string, **variables) if domain_translations else string % variables

def get_language_codes():
    language_codes = []
    for folder in os.listdir(_translations_dir):
        locale_dir = os.path.join(_translations_dir, folder, 'LC_MESSAGES')
        if not os.path.isdir(locale_dir):
            continue
        language_codes.append(folder)
    return language_codes

def init_translations(babel):
    if babel:
        babel._default_domain = domain_translations

        # Install a language selector if one has not yet been installed
        if babel.locale_selector_func is None:
            # Define a language selector
            def get_locale():
                # Retrieve a list of available language codes
                available_language_codes = get_language_codes()
                # Match list with languages from the user's browser's accept header
                language_code = request.accept_languages.best_match(available_language_codes)
                return language_code

            # Install the language selector
            babel.locale_selector_func = get_locale
