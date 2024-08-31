from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user_status = models.BooleanField(default=True)
    profile_pic = models.CharField(max_length=100)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'user_type']

    def save(self, *args, **kwargs):
        # Check if the password needs to be hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(UserAccount, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class RefreshToken(models.Model):
    token = models.CharField(max_length=255, unique=True)  # Store the token value
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)  # Link to the User model
    created_at = models.DateTimeField(auto_now_add=True)  # When the token was created
    expires_at = models.DateTimeField()  # When the token expires

    def __str__(self):
        return f"RefreshToken(user={self.user}, token={self.token})"