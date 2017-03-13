import string
import random
from django.db import models
from django.conf import settings
#from accounts.models import User
from time import gmtime, strftime

# Create your models here.

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



""" ==========================================================
    For generating folder destination and unique filename
========================================================== """

def generate_code(size=10, chars=string.ascii_uppercase + string.digits):

    return ''.join(random.choice(chars) for i in range(size))

def media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<MEDIA_TYPE>/<year>-<month>-<date>/<user_id>_<media_id>
    return '{0}/{1}/{2}/{3}_{4}'.format(settings.MEDIA_ROOT,instance.media_type, strftime("%y-%m-%d", gmtime()), instance.user.user_id, instance.media_id)


""" ==========================================================
    data model for storing uploaded media information
========================================================== """

class Media(models.Model):
    MEDIA_TYPES = (
        ('image','Image'),
        ('gif','GIF'),
        ('video','Video'),
        ('audio','Audio'),
        ('pdf','PDF'),
        ('word','Word'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="user who uploaded the media")
    media_id = IDField(db_column='externalid')
    media_url = models.FileField(upload_to=media_directory_path, default='no-img.jpg', db_column='upload')
    media_type = models.CharField("type of media", max_length=10, choices=MEDIA_TYPES, db_column='type')
    created = models.DateTimeField("date and time account was created", auto_now_add=True, db_column='time')

    class Meta:
        ordering =('created',)
            
    def __str__(self):
        return self.media_url.url

    def __unicode__(self):
        return self.media_url.ur
