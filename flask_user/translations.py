""" This file contains functions to translate strings for Flask-User.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from flask import _request_ctx_stack, current_app

# To avoid requiring the Flask-Babel, Babel and speaklater packages,
# we check if the app has initialized Flask-Babel or not
def get_translations():
    # If there is no context:  return None
    ctx = _request_ctx_stack.top
    if not ctx:
        return None

    # If context exists and contains a cached value, return cached value
    if hasattr(ctx, 'flask_user_translations'):
        return ctx.flask_user_translations

    # If App has not initialized Flask-Babel: return None
    app_has_initalized_flask_babel = 'babel' in current_app.extensions
    if not app_has_initalized_flask_babel:  # pragma no cover
        ctx.flask_user_translations = None
        return ctx.flask_user_translations

    # Prepare search properties
    import os
    import gettext as python_gettext
    from flask_babel import get_locale, get_translations, support
    domain = 'flask_user'
    locales = [get_locale()]
    languages = [str(locale) for locale in locales]

    # See if translations exists in Application dir
    app_dir = os.path.join(current_app.root_path, 'translations')
    filename = python_gettext.find(domain, app_dir, languages)
    if filename:
        ctx.flask_user_translations = support.Translations.load(app_dir, locales, domain=domain)

    # See if translations exists in Flask-User dir
    else:
        flask_user_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translations')
        ctx.flask_user_translations = support.Translations.load(flask_user_dir, locales, domain=domain)

    return ctx.flask_user_translations.merge(get_translations())

def gettext(string, **variables):
    """ Translate specified string."""
    translations = get_translations()
    if translations:
        return translations.ugettext(string) % variables
    return string % variables

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
