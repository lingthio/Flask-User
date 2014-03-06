Internationalization
====================
Flask-User has encapsulated all user-facing messages and uses the Babel package
to customize or translate these messages.

Babel can customize built-in English messages by creating an English
translations file and customizing only the messages that needs customizing.

Babel can translate built-in English messages into another language by
creating a language specific translations file and translating each message
into the new language.

Customizing Messages
--------------------

Locate the python package installation directory

::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

| This tutorial assumes that it returend
| ```~/.virtualenvs/myapp/lib/python2.7/site-packages```

```~/.virtualenvs/myapp/lib/python2.7/site-packages/flask_user/translations/flask_user.pot```
file contains all messages extracted from the flask_user package.

We can convert the extraction file into a translations file using the ``pybabel init`` command.
Create an english translations file we'll use the language code '``en``' like so:

::

    # Warning: 'pybable init' will erase the translations/en/LC_MESSAGES/flask_user.po file!
    # Use 'pybabel update' to update a translations file instead.
    pybabel init -d translations -l en -D flask_user -i ~/.virtualenvs/myapp/lib/python2.7/site-packages/flask_user/translations/flask_user.pot

This should have created the following file:

::

    translations/en/LC_MESSAGES/flask_user.po

| To edit the translations file. We recommend using a translation editor such as Poedit
|       `Download poedit <http://www.poedit.net/download.php>`_
| If you run Mac OS 10.6 or older, you'll need to download `version 1.5 from here <http://sourceforge.net/projects/poedit/files/poedit/1.5/>`_.

Edit ``translations/en/LC_MESSAGES/flask_user.po`` with this editor and Save

We can compile translations files (.po) into compiled translations files (.mo) using the ``pybabel compile`` command.
Compile all the translations files like so:

::

    pybabel compile -d translations -D flask_user -f

Translating Messages
--------------------

Translating a message is very similar to customizing English messages.

Follow the instructions in `Customizing Messages`_ and replace '``en``' with the language
code of the language you wish to translate messages for.

For a list of language codes: `See the two-letter codes here <http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.
