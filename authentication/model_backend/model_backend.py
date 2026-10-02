from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class CustomModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate
    using either their email address or phone number.
    """

    def authenticate(
        self, request, email=None, phonenumber=None, password=None, **kwargs
    ):
        # Determine which identifier was actually passed in
        identifier = email or phonenumber

        if not identifier or not password:
            return None

        try:
            # Dynamically query using whichever field was provided
            query = Q(email=identifier) | Q(phonenumber=identifier)
            user = User.objects.get(query)
        except User.DoesNotExist:
            # Run password hash check even if user doesn't exist to prevent timing attacks
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Safety check in case data integrity issues occur
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
