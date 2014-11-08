Internationalization
====================
Flask-User allows the developer to translate their user account management forms
into other languages. This allows us to:

* Customize built-in English text to custom English text
* Translate built-in English text into another language

Flask-User ships with the following languages:
* English (en)
* Chinese (Simplified) (zh, v0.6.1 and up)
* Dutch (nl)
* French (fr, v0.6.1 and up)


REQUIRED: Installing Flask-Babel
--------
Flask-User relies on the Flask-Babel package to translate the account management forms.
Without Flask-Babel installed, these forms WILL NOT BE translated.

Install Flask-Babel with

::

    pip install Flask-Babel


REQUIRED: Initializing Flask-Babel
--------

Flask-Babel must be initialized just after the Flask application has been initialized
and after the application configuration has been read:

::

    from flask.ext.babel import Babel

    ...

    app = Flask(__name__)
    app.config.from_object('app.config.settings')

    ...

    # Initialize Flask-Babel
    babel = Babel(app)

    # Use the browser's language preferences to select an available translation
    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)


How Flask-Babel works
---------------------
* Flask-Babel calls a translatable string a 'Message'.
* Messages are marked with ``gettext('string')``, ``_('string')``  or ``{%trans%}string{%endtrans%}``.
* ``pybabel extract`` extracts Messages into a ``.pot`` template file.
* ``pybabel update`` converts the ``.pot`` template file into a language specific
  ``.po`` translations file.

  * A ``.po`` file contains ``msgid/msgstr`` (key/value) pairs for each translatable string
  * The ``msgid`` represents the built-in English message (key)
  * The ``msgstr`` represents the translated message (value)

* Translators edit the ``msgstr`` portion of the ``.po`` translation files.
* ``pybabel compile`` compiles human readable ``.po`` translation files
  into machine readable ``.mo`` complied translation files.
* At runtime:

  * the browser specifies the preferred language code (``'en'`` for English, ``'es'`` for Spanish,
    ``'nl'`` for Dutch, etc.).
  * The web server loads the corresponding compiled translation file.
    For example: ``app/translations/en/LC_MESSAGES/flask_user.mo``.
  * gettext('string') looks up the ``msgid=='string'`` entry in the ``.mo`` file.
  * If a ``msgstr`` is defined: it will return the translated message, if not: it will return
    the built-in English message.


Preparing for translation
-------------------------
We need to copy the Flask-User ``translations`` directory to your application directory.

Flask-User typically installs in the ``flask_user`` sub-directory of the Python packages directory.
The location of this directory depends on Python, virtualenv and pip
and can be determined with the following command::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

Let's assume that:

* The Python packages dir is: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/``
* The Flask-User dir is: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/``
* Your app directory is: ``~/path/to/YOURAPP/YOURAPP``
  (your application directory typically contains the 'static' and 'templates' sub-directories).

Copy the ``translations`` directory from flask_user to your application directory::

    cd ~/path/to/YOURAPP/YOURAPP
    cp -r ~/.virtualenvs/YOURENV/lib/python2.7/site-packages/flask_user/translations .

| To edit the translations file. We recommend using a translation editor such as Poedit
|       `Download poedit <http://www.poedit.net/download.php>`_
| If you run Mac OS 10.6 or older, you'll need to download
  `version 1.5 from here <http://sourceforge.net/projects/poedit/files/poedit/1.5/>`_.

Customizing Messages
--------------------
Customization is achieved by 'translating' built-in English messages to
the custom English messages of your choice.
The two-letter language code for English is 'en'.

**Customize .po file**

Edit ``translations/en/LC_MESSAGES/flask_user.po``

We recommend using a translation program such as ``poedit``. If you want to edit
the .po file manually make sure to leave ``msgid`` strings as-is and to
only edit the ``msgstr`` strings.

Customize only those message that need to be different from the built-in message.
Entries with an empty ``msgstr`` will display the built-in ``msgid``.

Safe the .po file when you're done.

**Compile .mo file**

Compile a .mo compiled translation file from a .po translation file like so::

    cd ~/path/to/YOURAPP/YOURAPP
    pybabel compile -d translations -D flask_user -f

**Verify**

``.mo`` files are read when your web server starts, so make sure to restart your web server.

Point your browser to your app and your custom messages should appear.

Translating Messages
--------------------

**Determine the language code**

The ISO 639-1 standard defines two-letter codes for languages.
`Find your two-letter codes here <http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.

This document assumes that you chose 'es' for Spanish.

**Create .po file (One-time only)**

.po translation files are generated from .pot template files using ``pybabel init``.

::

    cd ~/path/to/YOURAPP/YOURAPP
    pybabel init -d translations -l es -D flask_user -i translations/flask_user.pot

**Update .po files**

The ``pybabel init`` command will over-write any existing .po files.

If you need to update the .po files (for example if a new Flask-User version
releases a new flask_user.pot template file), you can use the ``pybabel update``
command to keep your prior translations.

::

    cd ~/path/to/YOURAPP/YOURAPP
    pybabel update -d translations -l es -D flask_user -i translations/flask_user.pot

**Translate .po file**

Edit ``translations/es/LC_MESSAGES/flask_user.po``

We recommend using a translation program such as ``poedit``. If you want to edit
the .po file manually make sure to leave ``msgid`` strings as-is and to
only edit the ``msgstr`` strings.

Safe the .po file when you're done.

**Compile .mo file**

Compile a .mo compiled translation file from a .po translation file like so::

    cd ~/path/to/YOURAPP/YOURAPP
    pybabel compile -d translations -D flask_user -f

**Verify**

Make sure you have this code somewhere::

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

Make sure to prioritize the Spanish language in your browser settings.

``.mo`` files are read when your web server starts, so make sure to restart your web server.

Point your browser to your app and your translated messages should appear.


Troubleshooting
--------
If the code looks right, but the account management forms are not being translated:

* Check to see if the 'Flask-Babel' package has been installed (try using ``pip freeze``).
* Check to see if the browser has been configured to prefer the language you are testing.
* Check to see if the 'translations/' directory is in the right place.

