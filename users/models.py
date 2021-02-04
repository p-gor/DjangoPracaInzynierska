from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, first_name=None, last_name=None):
        if not username:
            raise ValueError("Wymagane jest podanie nazwy użytkownika")
        if not email:
            raise ValueError("Wymagane jest podanie adresu email użytkownika")
        if not password:
            raise ValueError("Wymagane jest podanie hasła użytkownika")
        if not first_name:
            raise ValueError("Wymagane jest podanie imienia użytkownika")
        if not last_name:
            raise ValueError("Wymagane jest podanie nazwiska użytkownika")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, first_name=None, last_name=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="adres e-mail", max_length=60, unique=True)
    username = models.CharField(verbose_name="nazwa użytkownika", max_length=40, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(verbose_name="imię", max_length=30)
    last_name = models.CharField(verbose_name="nazwisko", max_length=30)
    type_account = models.BooleanField(default=True, blank=True)
    # 0 - klient
    # 1 - Pentester

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return str(self.first_name + " " + self.last_name)

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


def validate_image(image):
    file_size = image.file.size

    limit_mb = 8
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Maksymalna wielkość pliku to %s MB" % limit_mb)


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profiles_picture_folder', validators=[validate_image])

    def __str__(self):
        return f'{self.user.username} Profile'
