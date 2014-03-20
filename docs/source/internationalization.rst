Internationalization
====================
Flask-User has encapsulated all user-facing messages and uses the Babel package
to customize or translate these messages.

Flask-User ships with a Dutch translation, and allows all messages to be
translated to any other language.

English message customization is achieved by 'translating' built-in english
messages to custom english messages.

Preparing for translations
--------------------------
We need to copy Flask-User's ``translations`` directory to your application directory.

Locate the python package installation directory::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

| This document assumes that it returned:
| ``~/.virtualenvs/YOURAPP/lib/python2.7/site-packages``
| and that your application directory is:
| ``~/path/to/YOURAPP``
| (your application directory typically has a 'templates' sub-directory).

Copy the ``translations`` directory from flask_user to your application directory::

    cd ~/path/to/YOURAPP
    cp -r ~/.virtualenvs/YOURAPP/lib/python2.7/site-packages/flask_user/translations .

| To edit the translations file. We recommend using a translation editor such as Poedit
|       `Download poedit <http://www.poedit.net/download.php>`_
| If you run Mac OS 10.6 or older, you'll need to download `version 1.5 from here <http://sourceforge.net/projects/poedit/files/poedit/1.5/>`_.

Customizing Messages
--------------------
Customization is achieved by 'translating' built-in English messages to
the custom English messages of your choice.
The two-letter language code for English is 'en'.

**Customize .po file**

Edit ``translations/en/LC_MESSAGES/flask_user.po``

Customize any message that you wish to customize. Leave the translations of other messages empty.
Safe the .po file when you're done.

**Compile .mo file**

Compile a .mo compiled translation file from a .po translation file like so::

    cd ~/path/to/YOURAPP
    pybabel compile -d translations -D flask_user -f

**Verify**

Restart your application and your custom messages should appear.

Translating Messages
--------------------

**Determine the language code**

The ISO 639-1 standard defines two-letter codes for languages.
`Find your two-letter codes here <http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.

This document assumes that you chose 'es' for Spanish.

**Create .po file**

::

    cd ~/path/to/YOURAPP
    pybabel init -d translations -l es -D flask_user -i translations/flask_user.pot

Note that the above command overwrites the file ``translations/es/LC_MESSAGES/flask_user.po``.
If you meant to update an existing file use ``pybabel update`` instead of ``pybabel init``.

**Translate .po file**

Edit ``translations/es/LC_MESSAGES/flask_user.po``

Translate any message that you wish to translate. Safe the .po file when you're done.

**Compile .mo file**

Compile a .mo compiled translation file from a .po translation file like so::

    cd ~/path/to/YOURAPP
    pybabel compile -d translations -D flask_user -f

**Verify**

Make sure you have this code somewhere::

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

Make sure to prioritize the Spanish language in your browser settings.

Restart your application and your translations should appear.

