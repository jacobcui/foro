from django.db import models

# Create your models here.
from django.conf import settings

from localflavor.au.models import AUStateField, AUPhoneNumberField
from easy_thumbnails.fields import ThumbnailerImageField

from django.utils.functional import LazyObject
from django.core.files.storage import get_storage_class

class AvatarStorage(LazyObject):
    def _setup(self):
        AVATAR_FILE_STORAGE = getattr(settings, 'AVATAR_FILE_STORAGE', settings.DEFAULT_FILE_STORAGE)
        self._wrapped = get_storage_class(AVATAR_FILE_STORAGE)()

avatar_storage = AvatarStorage()

ADR_TYPES = (
    ('Home', 'Home'),
    ('Work', 'Work'),
)

TEL_TYPES = (
    ('Mobile', 'Mobile'),
    ('Work', 'Work'),
    ('Fax', 'Fax'),
    ('Skype', 'Skype'),
)

EMAIL_TYPES = (
    ('Home', 'Home'),
    ('Work', 'Work'),
)

WEBSITE_TYPES = (
    ('Work', 'Work'),
    ('Personal', 'Personal'),
    ('Portfolio', 'Portfolio'),
    ('Blog', 'Blog'),
)

SOCNET_TYPES = (
    ('Skype', 'Skype'),
    ('Twitter', 'Twitter'),
    ('LinkedIn', 'LinkedIn'),
    ('Facebook', 'Facebook'),
    ('Pinterest', 'Pinterest'),
)

social_net_prefixes = dict(
    Skype = 'skype:',
    Twitter = 'https://twitter.com/',
    LinkedIn = 'http://linkedin.com/',
    Facebook = 'http://www.facebook.com/',
    Pinterest = 'http://www.pinterest.com/',
)


class Contact(models.Model):
    last_name = models.CharField(max_length = "40", blank=False)
    first_name = models.CharField(max_length = "40", blank=False)
    middle_name = models.CharField(max_length = "40", blank = True)
    title = models.CharField(max_length = "40", blank = True)
    organization = models.CharField(max_length = "50", blank = True)
    url = models.URLField( blank = True)    
    blurb = models.TextField(null=True, blank=True)
    profile_image = ThumbnailerImageField(upload_to=settings.PROFILE_IMAGE_DIRECTORY, blank=True, null=True)
    qr_image = models.ImageField(upload_to="qr_images/", blank=True, null=True)
    twitter_handle = models.CharField(max_length = "50", blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        self.profile_image.storage = avatar_storage
        self.profile_image.thumbnail_storage = avatar_storage

    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.last_name, self.organization)

class Address(models.Model):
    contact = models.ForeignKey(Contact)
    street = models.CharField(max_length = "50")
    city = models.CharField(max_length = "40")
    state = AUStateField()
    zip = models.CharField(max_length = "10") 
    type = models.CharField(max_length="20", choices = ADR_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s: %s %s, %s' % (self.contact.first_name, self.contact.last_name, self.street, self.city, self.state)

class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact)
    phone = models.CharField(max_length="20")
    type = models.CharField(max_length="20", choices = TEL_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s: %s" % (self.contact.first_name, self.contact.last_name, self.phone)
   
class Email(models.Model):
    contact = models.ForeignKey(Contact)
    email = models.EmailField() 
    type = models.CharField(max_length="20", choices = EMAIL_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s: %s" % (self.contact.first_name, self.contact.last_name, self.email)

class Website(models.Model):
    contact = models.ForeignKey(Contact)
    website = models.URLField( blank = True)
    type = models.CharField(max_length="20", choices = WEBSITE_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s: %s" % (self.contact.first_name, self.type, self.website)

class SocialNetwork(models.Model):
    contact = models.ForeignKey(Contact)
    handle = models.CharField(max_length = "50")
    type = models.CharField(max_length="20", choices = SOCNET_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    @property
    def url(self):
        prefixes = social_net_prefixes
        prefix = getattr(settings, '%s_PREFIX' % self.type.upper(), prefixes[self.type])
        return '%s%s' % (prefix, self.handle)

    def __unicode__(self):
        return "%s %s: %s" % (self.contact.first_name, self.type, self.handle)