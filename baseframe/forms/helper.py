from .validators import IsPublicEmailDomain, ValidationError

__all__ = ['is_public_email_domain']


class DummyField(object):
    # Validators need a field param to work, we're going to pass a dummy
    # https://github.com/wtforms/wtforms/blob/master/tests/validators.py#L14
    def __init__(self, data):
        self.data = data


def is_public_email_domain(email_or_domain):
    """
    Checks if the given email address or domain belongs to a public email domain
    """
    try:
        validator = IsPublicEmailDomain()
        # custom validators need to accept a form and field to work
        # as our validator doesn't do anything with the form, can just pass a dummy object
        validator(dict(), DummyField(email_or_domain))
    except ValidationError:
        return False
    return True
