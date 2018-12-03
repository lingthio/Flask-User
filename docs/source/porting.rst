Porting v0.6 to v0.9+
=====================
.. include:: includes/submenu_defs.rst
.. include:: includes/porting_submenu.rst

--------

Ever since Flask-User v0.4, we had plans to improve Flask-User but were held back
by our desire to maintain backwards compatibility for a while.

With Flask-User v1.0 (and its v1.0 alpha/beta) we decided it was time to move forward,
breaking compatibility with v0.6.

Porting slightly customized v0.6 applications
---------------------------------------------
If you've only customized Flask-User v0.6 in the following ways:

    - Changed ``USER_...`` app config settings
    - Customized form templates (the .html files)
    - Customized email templates (the .html or .txt files)

Reading :doc:`porting_basics` will suffice.

Porting highly customized v0.6 applications
-------------------------------------------
If you have:

    - Specified custom form classes (the .py files)
    - Specified custom view functions
    - Specified custom password or username validators
    - Specified a custom TokenManager
    - Used the optional UserAuth class

you will also need to read: :doc:`porting_customizations`.

Porting Tips
------------
See :doc:`porting_advanced`

--------

.. include:: includes/porting_submenu.rst
