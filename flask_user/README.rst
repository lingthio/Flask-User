Design overview
===============

The Core Logic shields itself from non-core services through the use
of Manager Interfaces.

- The TokenManager generates and verifies tokens.
- The PasswordManager hashes and verifies passwords
- The EmailManager sends email messages
- The DbManager adds, updates and deletes objects on a database.

::

             +-------+
             |       |  || TokenManager
             |       |
             | Core  |  || PasswordManager
   Views ||  |       |
             | Logic |  || EmailManager
             |       |
             |       |  || DbManager
             +-------+

- hash_password(password)
- verify_password(password, password_hash)


        TokenManager Interface    PasswordManager Iface
    +---======================----======================---++
    |                                                      ||
    |                      Core Logic                      ||  Views
    |                                                      ||
    +---======================----======================---++
        DbManager Interface       EmailManager Interface

        ======================    ======================
        DbAdapter Interface       EmailMailer Interface
        - DynamoDbAdapter         - SendgridEmailMailer
        - MongoDbAdapter          - SendmailEmailMailer
        - SQLDbAdapter            - SMTPEmailMailer
