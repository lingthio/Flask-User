from passlib.context import CryptContext

def init_password_crypt_context():
    """
    Initialize passlib CryptContext.

    See http://pythonhosted.org/passlib/new_app_quickstart.html
    """
    # Customizable passlib crypt context
    crypt_context = CryptContext(
            schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'],
            default='bcrypt',
            all__vary_rounds = 0.1,
            )
    return crypt_context

