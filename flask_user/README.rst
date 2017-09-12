Design overview
===============
The Core Logic shields itself from non-core services through the use
of Manager Interfaces (DB/Email/Password/Token Managers).

- The DBManager manages objects in a database.
- The EmailManager sends email messages
- The PasswordManager hashes and verifies passwords
- The TokenManager generates and verifies tokens.

The DBManager shields itself from specific database services
(DynamoDB/MongoDB/SQL) through the use of the DbAdapter interface.

The EmailManager shields itself from specific email services
(SendGrid/Sendmail/SMTP) through the use of the EmailAdapter interface.

Because the core logic is relatively small, we decided to simply
include the core logic with the DBManager.

::

                     Views

    +-------- =================== -------------------------------------------+
    |         DBManager interface                                            |
    |                                                                        |
    |         DBManager and Core Logic                                       |
    |                                                                        |
    |                 +------------------------------------------------------+
    |                 |
    |                 |     ============    ===============    ============
    |                 |     EmailManager    PasswordManager    TokenManager
    |                 |     Interface       Interface          Interface
    |                 |    +------------+  +---------------+  +------------+
    |                 |    |EmailManager|  |PasswordManager|  |TokenManager|
    +-----------------+    +------------+  +---------------+  +------------+

    ===================     =================
    DbAdapter               EmailAdapter
    Interface               Interface

    - DynamoDbAdapter       - SendGridAdapter
    - MongoDbAdapter        - SendmailAdapter
    - SQLDbAdapter          - SMTPAdapter

