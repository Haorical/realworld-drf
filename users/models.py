import jwt
from django.db import models
# from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin  # 导错包了
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  # 导错包了
from django.conf import settings


class UserManager(BaseUserManager):

    def creat_user(self, username, email, password=None):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        """
      Create and return a `User` with superuser powers.
      Superuser powers means that this use is an admin that can do anything
      they want.
      """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    # bio = models.TextField()
    # image = models.URLField(null=True, blank=True)

    # followers = models.ManyToManyField('self', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self): return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self): return self.username

    def get_short_name(self): return self.username

    def _generate_jwt_token(self):
        token = jwt.encode(
            {
                'id': self.pk,
                'exp': 1672502400,
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return token
