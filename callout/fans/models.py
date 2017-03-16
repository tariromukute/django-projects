import string
import random
from time import gmtime, strftime
from django.db import models
from django.conf import settings

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

class Fan(models.Model):
    o_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='f_o_user', verbose_name="user being followed")
    x_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='f_x_user', verbose_name="user following")
    seen = models.BooleanField("user seen new fan", default=False, db_column='seen')
    created = models.DateTimeField("date and time user followed x_user", auto_now_add=True, db_column='time')

    class Meta:
        unique_together = ('o_user', 'x_user')
        ordering = ('created',)


class Request(models.Model):
    STATUS_TYPES = (
        ('A', 'accepted'),
        ('D', 'declined'),
        ('P', 'pending'),
    )
    request_id = IDField(db_column='externalid')
    o_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='r_o_user', verbose_name="user receiving the follow request")
    x_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='r_x_user', verbose_name="user sending the follow request")
    request_status = models.CharField("follow request status", max_length=2, default='P', choices=STATUS_TYPES, db_column='status')
    created = models.DateTimeField("date and time user followed x_user", auto_now_add=True, db_column='time')

    class Meta:
        unique_together = ('o_user', 'x_user')
        ordering = ('created',)

    
