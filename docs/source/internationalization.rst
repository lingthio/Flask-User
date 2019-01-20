Internationalization
====================
Flask-User ships with the following language translations:

* Chinese Simplified (zh)
* Dutch (nl)
* English (en)
* German (de)
* Farsi (fa)
* Finnish (fi)
* French (fr)
* Italian (it)
* Russian (ru)
* Spanish (es)
* Swedish (sv)
* Turkish (tr)

They can be found in the Flask-User installation directory, under the ``translations`` subdirectory.
Each translation file is called ``flask_user.mo`` (called a domain translation)
to differentiate from your application's translations, typically called ``messages.mo``

REQUIRED: Installing Flask-BabelEx
----------------------------------
There are two distinct Flask extensions for managing translations: ``Flask-Babel``
and ``Flask-BabelEx``.

Flask-User relies on the domain-specific abilities of ``Flask-BabelEx``
and will not translate with ``Flask-Babel``::

    # Uninstall Flask-Babel if needed
    pip uninstall Flask-Babel

    # Install Flask-BabelEx
    pip install Flask-BabelEx

REQUIRED: Initializing Flask-BabelEx
------------------------------------

Flask-BabelEx must be initialized:

    - After Flask-User initialization
    - After the app config has been loaded
    - Before Flask-User initialization

Example::

    from flask import Flask, request
    from flask_babelex import Babel
    from flask_user import UserManager
        ...
    # Setup Flask
    app = Flask(__name__)
        ...
    # Read applicaton config
    app.config.from_object('app.config.settings')
        ...
    # Initialize Flask-BabelEx
    babel = Babel(app)
        ...
    # Initialize Flask-User
    user_manager = UserManager(app, db, User)

REQUIRED: Setting your browser language preference
--------------------------------------------------
You will need to add and prioritize one of the Flask-User supported languages
in your browser.

For Google Chrome:

- Chrome > Preferences. Search for 'Language'.
- Expand the 'Language' bar > Add languages.
- Check the 'Dutch' checkbox > Add.
- Make sure to move it to the top: Three dots > Move to top.

You can test this with the :doc:`basic_app`.
