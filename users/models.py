from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import validate_email


class CustomUserManager(UserManager):

    def _get_email(self, email: str):
        validate_email(email)
        return self.normalize_email(email)

    def _create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        commit: bool,
        is_staff: bool = False,
        is_superuser: bool = False
    ):

        email = self._get_email(email)

        user = User(email=email, username=email, first_name=first_name, last_name=last_name,
                    is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)

        if commit:
            user.save()

        return user

    def create_superuser(self, email: str, password: str, commit: bool = True):
        return self._create_user(email, password, is_staff=True, is_superuser=True, commit=commit)

    def create_user(self, email: str, first_name: str, last_name: str, password: str, commit: bool = True):
        return self._create_user(email, first_name, last_name, password, commit=commit)


class User(AbstractUser):

    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    bio = models.TextField(max_length=200, null=True, blank=True)
    follower_count = models.IntegerField(default=0, null=True)
    following_count = models.IntegerField(default=0, null=True)
    profile_picture = models.ImageField(null=False, blank=True, upload_to="images")

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [first_name, last_name]

    objects = CustomUserManager()

    def profile_link(self):
        user_id = str(self.id)
        user_name_combo = (self.first_name + self.last_name + user_id).lower()
        return user_name_combo


#class CustomUserManager(UserManager):
#
#    def _get_email(self, email: str):
#        validate_email(email)
#        return self.normalize_email(email)
#
#    def _create_user(
#        self,
#        email: str,
#        first_name: str,
#        last_name: str,
#        password: str,
#        commit: bool,
#        is_staff: bool = False,
#        is_superuser: bool = False
#    ):
#
#        email = self._get_email(email)
#
#        user = User(email=email, username=email, first_name=first_name, last_name=last_name,
#                    is_staff=is_staff, is_superuser=is_superuser)
#        user.set_password(password)
#
#        if commit:
#            user.save()
#
#        return user
#
#    def create_superuser(self, email: str, password: str, commit: bool = True):
#        return self._create_user(email, password, is_staff=True, is_superuser=True, commit=commit)
#
#    def create_user(self, email: str, first_name: str, last_name: str, password: str, commit: bool = True):
#        return self._create_user(email, first_name, last_name, password, commit=commit)
#
#
#class User(AbstractUser):
#
#    email = models.EmailField(unique=True, blank=False, null=False)
#    first_name = models.CharField(max_length=20, blank=False, null=False)
#    last_name = models.CharField(max_length=20, blank=False, null=False)
#
#    USERNAME_FIELD = "email"
#
#    REQUIRED_FIELDS = [first_name, last_name]
#
#    objects = CustomUserManager()





















#class CustomUserManager(UserManager):
#
#    def _get_email(self, email: str):
#        validate_email(email)
#        return self.normalize_email(email)
#
#    def _create_user(
#        self,
#        email: str,
#        password: str,
#        commit: bool,
#        is_staff: bool = False,
#        is_superuser: bool = False
#    ):
#
#        email = self._get_email(email)
#
#        user = User(email=email, username=email,
#                    is_staff=is_staff, is_superuser=is_superuser)
#        user.set_password(password)
#
#        if commit:
#            user.save()
#
#        return user
#
#    def create_superuser(self, email: str, password: str, commit: bool = True):
#        return self._create_user(email, password, is_staff=True, is_superuser=True, commit=commit)
#
#    def create_user(self, email: str, password: str, commit: bool = True):
#        return self._create_user(email, password, commit=commit)
#
#
#class User(AbstractUser):
#
#    email = models.EmailField(unique=True, blank=False, null=False)
#
#    USERNAME_FIELD = "email"
#
#    REQUIRED_FIELDS = []
#
#    objects = CustomUserManager()
#