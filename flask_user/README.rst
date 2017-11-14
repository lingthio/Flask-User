Design overview
===============
The Core Logic shields itself from non-core services through the use
of Manager Interfaces.

- The DBManager manages objects in a database.
- The EmailManager sends email messages
- The PasswordManager hashes and verifies passwords
- The TokenManager generates and verifies tokens.

The DBManager shields itself from specific database services
through the use of the DbAdapter interface.
Flask-User ships with the following implementations::

- DynamoDbAdapter
- MongoDbAdapter
- SQLDbAdapter

The EmailManager shields itself from specific email services
through the use of the EmailAdapter interface.
Flask-User ships with the following implementations::

- SendgridEmailAdapter
- SendmailEmailAdapter
- SMTPEmailAdapter

Because the core logic is relatively small, we decided to simply
include the core logic with the DBManager.

::

                                    Views

    +----------------------- =================== ----------------------------+
    |                        DBManager interface                             |
    |                                                                        |
    |                      DBManager and Core Logic                          |
    |                                                                        |
    |               +--------------------------------------------------------+
    |               |
    |               |    ==============    =================    ==============
    |               |    EmailManager      PasswordManager      TokenManager
    |               |    Interface         Interface            Interface
    |               |    +------------+    +---------------+    +------------+
    |   DBManager   |    |EmailManager|    |PasswordManager|    |TokenManager|
    +---------------+    +------------+    +---------------+    +------------+

    =================    ==============
    DbAdapter            EmailAdapter
    Interface            Interface

    - DynamoDbAdapter    - SendgridEmailAdapter
    - MongoDbAdapter     - SendmailEmailAdapter
    - SQLDbAdapter       - SMTPEmailAdapter

