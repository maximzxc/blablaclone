from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django_markdown.models import MarkdownField
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_superuser, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_superuser=is_superuser,
            is_staff=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)


class City(models.Model):
    name = models.CharField(
        blank=False,
        max_length=150,
        unique=True,
    )

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        # TODO: add proper path
        return "/"


class Ride(models.Model):
    from_city = models.ForeignKey(
        'City',
        related_name='city_rides',
        blank=False,
        null=False,
    )
    to_city = models.ForeignKey(
        'City',
        related_name='city_rides2',
        blank=False,
        null=False,
    )
    departure_time = models.DateTimeField(
        blank=False,
        null=False,
        unique=False,
        auto_now=False,
        auto_now_add=False,
    )
    will_visit = models.ManyToManyField(
        'City',
        related_name='city_rides3',
        blank=False,
        null=False,
    )
    free_places = models.PositiveIntegerField(
        blank=False,
        null=False,
        unique=False,
    )
    driver = models.ForeignKey(
        'User',
        related_name='user_rides',
        blank=False,
        null=False,
    )
    passangers = models.ManyToManyField(
        'User',
        related_name='user_rides2',
        blank=False,
        null=False,
    )
    price = models.PositiveIntegerField(
        blank=False,
        null=False,
        unique=False,
    )
    slug = AutoSlugField(
        populate_from='title',
        blank=False,
        null=False,
        unique=True,
    )
    title = models.CharField(
        blank=False,
        max_length=150,
        unique=False,
    )

    def __unicode__(self):
        return unicode(self.title[:50])

    def get_absolute_url(self):
        # TODO: add proper path
        return "/"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=150,
        blank=False,
        null=False,
    )
    name = models.CharField(
        blank=False,
        max_length=150,
        unique=False,
    )
    surname = models.CharField(
        blank=False,
        max_length=150,
        unique=False,
    )
    car = models.CharField(
        blank=True,
        max_length=150,
        unique=False,
    )
    phone = models.CharField(
        blank=True,
        max_length=150,
        unique=False,
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
        unique=False,
        auto_now=False,
        auto_now_add=False,
    )
    about = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='images',
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(default=False, editable=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return unicode(self)

    def get_short_name(self):
        return unicode(self)

    def __unicode__(self):
        return unicode(self.name[:50])

    def get_absolute_url(self):
        # TODO: add proper path
        return "/"


class RideRequest(models.Model):
    user = models.ForeignKey(
        'User',
        related_name='user_riderequests',
        blank=False,
        null=False,
    )
    ride = models.ForeignKey(
        'Ride',
        related_name='ride_riderequests',
        blank=False,
        null=False,
    )
    message = models.TextField(blank=False)

    def __unicode__(self):
        return u"RideRequest #%s" % self.id

    def get_absolute_url(self):
        # TODO: add proper path
        return "/"
