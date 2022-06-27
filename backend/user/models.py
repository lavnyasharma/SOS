
from cv001.utils.uid import encode_id
from datetime import datetime, timedelta
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone number must be set'))
        phone_number = phone_number
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone_number, password, **extra_fields)


class user(AbstractBaseUser, PermissionsMixin):
    """
    Auth User model 
    Key Features
    -   Phone number - Login Parameter as phone_number
    -   UID - User Id
    -   email_confirmed
    """
    UID = models.CharField(
        _('UID'),
        max_length=150,
        unique=True,
    )
    phoneno_regex = RegexValidator(
        regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', message="Please enter a valid Phone number")
    phone_number = models.CharField(_('phone'), validators=[
                                    phoneno_regex], max_length=17,
                                    unique=True,
                                    help_text=_('Enter a Phone number'),
                                    error_messages={'unique': 'a user with that Phone Number already exists.'})

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True, default=' ')
    email_confirmed = models.BooleanField(
        _('email active'),
        default=False,
        help_text=_(
            'Designates whether this user has confirmed his email '
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now=True)
    gender = models.CharField(_('gender'), max_length=10, choices=[
                              ('m', 'male'), ('f', 'female'), ('o', 'other')], blank=True)
    age = models.IntegerField(_('age'), null=True)
    address = models.CharField(_("address"), max_length=300, blank=True)
    pin = models.CharField(_("pin"), max_length=17, blank=True)
    is_doctor = models.BooleanField(
        _('Doctor active'),
        default=False,
        help_text=_(
            'Designates whether this user is a doctor or not'
        ),
    )
    user_Type = models.CharField(default="u",max_length=2,)
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def save(self, phone=None, *args, **kwargs):
        if phone != None:
            uid = encode_id(p=phone, ct=str(timezone.now()))
            self.UID = uid
        super(user, self).save(*args, **kwargs)

    def uid(self):
        return self.UID

    def __str__(self):
        return self.phone_number

    def get_phone(self):
        return self.phone_number

    def get_email(self):
        return self.email

    def get_active(self):
        return self.is_active

    def get_pincode(self):
        return self.PCID

    def get_address(self):
        return self.AID

    def get_fname(self):
        return self.first_name

    def get_lname(self):
        return self.last_name

    def email_stats(self, value):
        self.email_confirmed = value

    def get_email_status(self):
        return self.email_confirmed

    def Email(self):
        if self.email != None:
            if self.email_confirmed == True:
                return self.email
            raise Exception('email not confirmed')
        raise Exception('invalid email')

# Address model


class Address(models.Model):

    """
    Address model
    - AID (primary key)
    - UID (Foregin key)
    - address line one as address_line_one
    - address line two as address_line_two
    - address line three as address_line_three
    - address line four as address_line_four
    """
    AID = models.CharField(_("Address"), primary_key=True,
                           max_length=150, help_text=("Address id"),)
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id')
    )
    address_line_one = models.TextField(_("address line one"), blank=True)
    address_line_two = models.TextField(_("address line two"), blank=True)
    address_line_three = models.TextField(_("address line three"), blank=True)
    address_line_four = models.TextField(_("address line four"), blank=True)
    district = models.CharField(_("district"), blank=False, max_length=50)
    state = models.CharField(_("state"), blank=False, max_length=50)
    is_home = models.BooleanField(_("is home"), default=True)
    PCID = models.CharField(
        _('pincode id'),
        max_length=150,
        help_text=('pincode id'),

    )
    PHID = models.CharField(
        _('Phone no id '),
        max_length=150,
        help_text=('phoneno id')
    )
    created_on = models.DateField(_('created on'), auto_now=True)
    updated_on = models.DateField(_('updated on'), null=True)
    pincode_number = models.CharField(_('Pincode'), validators=[], max_length=17,
                                      help_text=_('Enter a Pincode'), default=None
                                      )
    address = models.CharField(_("address"), max_length=300, default=None)

    def aid(self):
        return self.AID

    def uid(self):
        return self.UID

    def phid(self):
        return self.PHID

    def pcid(self):
        return self.PCID

    def home(self):
        return self.is_home


# Phone number model

class PhoneNumber(models.Model):
    """
    Phone number model
    """
    phoneno_regex = RegexValidator(
        regex=r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', message="Please enter a valid Phone number")
    PHID = models.CharField(_("phone number id"),
                            max_length=150, primary_key=True)
    phone_number = models.CharField(_('phone'), validators=[
        phoneno_regex], max_length=15,
        help_text=_('Enter a Phone number'), null=False
    )
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id')
    )

    def phone(self):
        return self.phone_number

    def update(self, value):
        self.phone_number = value
        return self.phone_number

    def uid(self):
        return self.UID


# Pincode model

class Pincode(models.Model):
    """
    Pincode model
    """
    PCID = models.CharField(_("pincode id"),
                            max_length=150, primary_key=True, )
    pincode_number = models.CharField(_('Pincode'), validators=[], max_length=17,
                                      help_text=_('Enter a Pincode'), default=None
                                      )
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id')
    )

    def pincode(self):
        return self.pincode

    def Pcid(self):
        return self.PCID

    def uid(self):
        return self.UID


class EmailToken(models.Model):
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id'), unique=True
    )
    email = models.CharField(
        _("email"), max_length=100, null=False, unique=True)
    Conf_token = models.CharField(
        _("Token"), max_length=100, null=False, unique=True)
    created_on = models.DateTimeField(_("created"), auto_now=True)
    expiration = models.DateTimeField(
        _("expiration"), default=timezone.localtime()+timedelta(minutes=9))


class PasswordChangeRequestModel(models.Model):
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id'), unique=True
    )
    password = models.CharField(_("password"), max_length=50)
    token = models.CharField(_("conf token"), max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now=True)
    expiration = models.DateTimeField(
        _("expiration"), default=timezone.localtime()+timedelta(minutes=15))


class img(models.Model):
    image = models.ImageField(upload_to='images/user')

    def save(self, dict):
        if not self.id:
            self.image = compressImage2(self.image, dict)
        else:
            self.image = compressImage2(self.image, dict)
        super().save()


def compressImage2(images, dict):
    imageTemporary = Image.open(images)
    outputstream = BytesIO()
    imageTemporary2 = imageTemporary.crop(
        (dict['left'], dict['top'], dict['right'],  dict['bottom']))
    imageTemporary2.save(outputstream, format='JPEG', quality=40)
    outputstream.seek(0)
    images = InMemoryUploadedFile(outputstream, 'ImageField', "%s.jpg" % images.name.split('.')[
        0], 'image/jpeg', sys.getsizeof(outputstream), None)
    return images


class fmctoken(models.Model):
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id'), unique=True
    )
    pin = models.CharField(_("pin"), max_length=50,default="")
    token = models.CharField(_("conf token"), max_length=500)
    created_on = models.DateTimeField(_("created on"), auto_now=True)
    expiration = models.DateTimeField(
        _("expiration"), default=timezone.localtime()+timedelta(minutes=15))