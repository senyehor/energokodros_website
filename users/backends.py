from django.contrib.auth import backends


class AllowTryAuthenticateInactive(backends.ModelBackend):
    """This backend allows every registered user to try to be authenticated
     in order to display custom login message for users who did not confirm
     their email address (is_active=False)"""

    def user_can_authenticate(self, user):
        return True
