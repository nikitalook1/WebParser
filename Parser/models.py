from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class Website(models.Model):
    url = models.URLField()
    text_file = models.FileField(upload_to='texts/', null=True, blank=True)

class PageData(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    content = models.TextField()

class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер пользователя, где email является уникальным идентификатором
    для аутентификации вместо usernames.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Пользователи должны иметь логин'))
        if not email:
            raise ValueError(_('Пользователь должен иметь email адрес'))
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=150, unique=True, default='temporary_username')
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Дополнительные поля могут быть добавлены здесь

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    #REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        # Пользователь идентифицируется по email адресу
        return self.email

    def get_short_name(self):
        # Пользователь идентифицируется по email адресу
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        # Отправка email пользователю
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # Добавьте related_name аргументы для каждого поля
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )

