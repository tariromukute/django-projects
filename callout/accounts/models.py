import string
import random
from time import gmtime, strftime
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from medias.models import Media

# Create your models here.

# creates auth token when user signs in
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

""" NB: Need to deal with superuser case """
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, first_name, last_name, **extra_fields):

        """ Creates and saves a user with the given information """

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        #extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, first_name, last_name, **extra_fields)


""" ==========================================================
    For generating Custom External ID
========================================================== """
class IDField(models.CharField):

    def __init__(self, *args, **kwargs):
        #self.default = 'ccccc'
        kwargs['max_length'] = 30
        kwargs['default'] = self.generate_id()
        kwargs['unique'] = True
        super(IDField, self).__init__(*args, **kwargs)

    def generate_code(self, size=10, chars=string.ascii_uppercase + string.digits):

        return ''.join(random.choice(chars) for i in range(size))

    def generate_id(self):
        # generate probably unique UUID
        return '{0}{1}'.format(strftime('%y%W%d%S%M', gmtime()),self.generate_code())



class User(AbstractBaseUser):
    ACCOUNT_TYPES =(
        ('PVT','Private'),
        ('PUB','Public'),
    )
    email = models.EmailField("email address", unique=True)
    user_id = IDField()
    first_name = models.CharField("first name", max_length=30, db_column='fname')
    middle_name = models.CharField("middle name", max_length=30, blank=True, db_column='mname')
    last_name = models.CharField("last name", max_length=30, db_column='lname')
    display_picture = models.OneToOneField(Media, related_name="DP", null=True, verbose_name="user's display picture")
    cell_number = models.CharField("cell phone number", max_length=10, blank=True, db_column='cell')
    country = models.CharField("country of usual residence", max_length=20, blank=True, db_column='country')
    """ Put user profile picture and wallpaper """
    date_of_birth = models.DateField("date of birth", blank=True, db_column='dob')
    """ Consider separating the following 3 into a UserProfile table along with other prospective information """
    won = models.IntegerField("number of callouts the user won", default=0, db_column='won')
    drew = models.IntegerField("number of callouts the user drew", default=0, db_column='drew')
    lost = models.IntegerField("number of callouts the user lost", default=0, db_column='lost')
    code = models.CharField("code to verify email transactions", blank=True, max_length=20, db_column='code')
    account_type = models.CharField("type of user account", max_length=3, default='PUB', choices=ACCOUNT_TYPES, db_column='type')
    created = models.DateTimeField("date and time account was created", auto_now_add=True, db_column='time')
    is_active = models.BooleanField("active", default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):

        """ Returns fname plus lname separated by a space """
        return ('%s %s' % (self.first_name, self.last_name)).strip()

    def get_short_name(self):

        """ Returns fname of User as short name """
        return self.first_name

    def email_user(self, subject, message, from_mail='nhembe.culturalpride@gmail.com', **kwargs):

        """ Sends an email to this user """
        send_mail(subject, message, from_mail, [self.email], **kwargs)


