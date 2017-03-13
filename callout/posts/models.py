import string
import random
from time import gmtime, strftime
from django.db import models
from django.conf import settings
from medias.models import Media
from accounts.models import User

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



class Post(models.Model):
    POST_TYPES = (
        ('N', 'Native'),
        ('F', 'Facebook'),
        ('T', 'Twitter'),
        ('I', 'Instagram'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="user who created the post")
    post_id = IDField(db_column='externalid')
    medias = models.ManyToManyField(Media, verbose_name="list of media attached to post")
    title = models.CharField("the title of the post", max_length=150, blank=True, db_column='title')
    caption = models.TextField("description of post", blank=True, db_column='description')
    post_type = models.CharField("type of post", max_length=2, blank=False, default='N', db_column='type')
    created = models.DateTimeField("date and time post was created", auto_now_add=True, db_column='time')

class Reaction(models.Model):
    REACTION_TYPES = (
        (3, 'Fancy'),
        (5, 'Disapprove'),
        (7, 'Love'),
        (11, 'Hate'),
        (13, 'Sad'),
    )
    reaction_id = IDField(db_column='externalid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_reactor', verbose_name="user who reacted to the post")
    post = models.ForeignKey(Post, verbose_name="post that the user reacted to")
    reaction = models.IntegerField("type of reaction", default=0, choices=REACTION_TYPES, db_column='type')
    created = models.DateTimeField("date and time reaction was created", auto_now_add=True, db_column='time')

    class Meta:
        unique_together = ('post', 'user')
        ordering = ('created',)

class Remark(models.Model):
    REMARK_TYPES = (
        ('D', 'direct'),
        ('O', 'open'),
    )
    remark_id = IDField(db_column='externalid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_remarker', verbose_name="user who remarked on the post")
    post = models.ForeignKey(Post, verbose_name="post that the user remarked on")
    remark = models.TextField("remark on post", blank=False, db_column='remark')
    remark_type = models.CharField("type of remark", max_length=2, choices=REMARK_TYPES, db_column='type')
    created = models.DateTimeField("date and time reaction was created", auto_now_add=True, db_column='time')


