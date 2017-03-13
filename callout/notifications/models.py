import string
import random
from time import gmtime, strftime
from django.db import models
from django.conf import settings
from accounts.models import User
from posts.models import Post

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

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('Post_R', 'post_reaction'),
        ('Post_C', 'post_comment'),
        ('Post_DC','post_direct_comment'),
        ('Post_M', 'post_mention'),
        ('Callout_R', 'callout_reaction'),
        ('Callout_C', 'callout_comment'),
        ('Callout_CH', 'callout_challenge'),
        ('Callout_CA', 'callout_challenge_accepted'),
        ('Callout_CD', 'callout_challenge_declined'),
        ('Callout_DC','callout_direct_comment'),
        ('Callout_M', 'callout_mention'),
        ('Fan_F', 'fan_following'),
        ('Follow_A', 'follow_request_accepted'),
        ('Follow_D', 'follow_request_declined'),
    )
    notification_id = IDField(db_column='externalid')
    o_user = models.ForeignKey(User, related_name='o_user', verbose_name="user receiving notification")
    x_user = models.ForeignKey(User, related_name='user', verbose_name="user generating notification")
    type_id = models.CharField("id of the objected being notified on", max_length=30, blank=False, db_column='typeid')
    notification_type = models.CharField("type of notification", max_length=10, blank=False, choices=NOTIFICATION_TYPES, db_column='type')
    seen = models.BooleanField("notifation seen status", default=False, db_column='seen')
    created = models.DateTimeField("date and time callout was created", auto_now_add=True, db_column='time')

    class Meta:
        ordering = ('created',)
    

