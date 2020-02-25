from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from .managers import UserManager
from core.models import City


class Specialist(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    thumbnail = ImageSpecField(source='avatar', processors=[ResizeToFill(50, 50)], format='JPEG',
                               options={'quality': 60})  # create thumbnail image for user
    gender = models.CharField(max_length=255, choices=GENDER, default='Male')
    birth_date = models.DateField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    whatsapp = models.CharField(max_length=11, blank=True)
    specialist = models.ForeignKey(Specialist, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)

    facebook = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    google = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
