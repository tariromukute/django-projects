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


class Callout(models.Model):
    callout_id = IDField(db_column='externalid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_owner', verbose_name="user who created the post")
    #oposts = models.ManyToManyField(OPost, verbose_name="list of oposts challenged")
    title = models.CharField("title of callout", max_length=100, blank=True, db_column='title')
    is_active = models.BooleanField("whether all challenges have been reacted to", default=False)
    pub_date = models.DateTimeField("date and time callout should be published by", db_column='pub_date')
    created = models.DateTimeField("date and time callout was created", auto_now_add=True, db_column='time')

class Remark(models.Model):
    REMARK_TYPES = (
        ('D', 'Direct'),
        ('O', 'Open'),
    )
    remark_id = IDField(db_column='externalid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_remarker', verbose_name="user who remarked on the post")
    callout = models.ForeignKey(Callout, verbose_name="callout that the user remarked on")
    remark = models.TextField("remark on callout", blank=False, db_column='remark')
    remark_type = models.CharField("type of remark", max_length=2, choices=REMARK_TYPES, db_column='type')
    created = models.DateTimeField("date and time reaction was created", auto_now_add=True, db_column='time')

    class Meta:
        ordering = ('created',)


class OPost(models.Model):
    STATUS_TYPES = (
        ('A', 'accepted'),
        ('D', 'declined'),
        ('P', 'pending'),
    )
    """ id of callout challenge, unique_together with post """
    o_post_id = IDField(db_column='externalid')
    callout = models.ForeignKey(Callout, verbose_name="callout that posted has been challenged in")
    post = models.ForeignKey(Post, verbose_name="post challenged")
    post_status = models.CharField("status od post", max_length=2, default='P', choices=STATUS_TYPES, db_column='status')
    created = models.DateTimeField("date and time reaction was created", auto_now_add=True, db_column='time')

    class Meta:
        unique_together = ('callout', 'post')

class Reaction(models.Model):
    REACTION_TYPES = ( 
        (3, 'Fancy'),
        (5, 'Disapprove'),
        (7, 'Love'),
        (11, 'Hate'),
        (13, 'Sad'),
    )
    reaction_id = IDField(db_column='externalid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_reactor', verbose_name="user who reacted to the post")
    opost = models.ForeignKey(OPost, related_name='o_post', verbose_name="post that the user reacted to")
    reaction = models.IntegerField("type of reaction", default=0, choices=REACTION_TYPES, db_column='type')
    created = models.DateTimeField("date and time reaction was created", auto_now_add=True, db_column='time')

    class Meta:
        unique_together = ('opost', 'user')
        ordering = ('created',)
