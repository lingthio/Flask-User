Customization
=============
Flask-User has been designed with full customization in mind, and and here is a list of
behaviors that can be customized as needed:

Level One customization

* Customizing Features and Settings
* Customizing Endpoint URLs
* See :doc:`customize1`

Level Two customization

* Customizing Emails
* Customizing Field labels and Flash messages
* Customizing Form templates
* Customizing Validation messages
* See :doc:`customize2`

Level Three customization

* Customizing Password and Username validators
* Customizing Password hashing
* Customizing Token generation
* Customizing View functions
* See :doc:`customize3`

**Customization Levels**

We classify each customization based on the safety level and the coding effort involved.

**Level One Customizations** involve changing a setting in the application config.
These customizations have been well tested through our automated tests
and can be applied safely.
See :doc:`customize1`

**Level Two Customizations** require editing a non-Python file such as a template file
or a Babel translation file.
Mistakes in these files are visible to customers
but it's unlikely that they will endanger the stability of your website.
See :doc:`customize2`

**Level Three Customizations** require editing of Python files.

They can often affect the stability of Flask-User and of your website.
You must rely on your own testing to make sure that Flask-User operations have not been broken.
See :doc:`customize3`


.. toctree::
    :maxdepth: 1

    customize1
    customize2
    customize3
