import datetime
#from django.db import models
from rest_framework import serializers
from posts.models import Post as PostModel, Remark as RemarkModel, Reaction as ReactionModel
from medias.serializers import MediaSerializer
from accounts.serializers import UserSerializer
#Create ModelSerializer classes

class DateSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return '%Y-%m-%d' % (value.year, value.month, value.day)
    
class DateTimeSerializer(serializers.ModelSerializer):
    
    date = DateSerializer(many=False, read_only=True)
    
    class Meta:
        model = datetime
        fields = ('minute', 'hour', 'date')
        
    
class PostSerializer(serializers.ModelSerializer):

    created = DateTimeSerializer(many=False)
    medias = MediaSerializer(many=True)
    user = UserSerializer(many=False)
    
    class Meta:
        model = PostModel
        fields = ('user', 'post_id', 'title', 'caption', 'medias', 'created')
        readonly_fields = ()

class EmbeddedPostSerializer(serializers.ModelSerializer):

    medias = MediaSerializer(many=True)
    user = UserSerializer(many=False)
    
    class Meta:
        model = PostModel
        fields = ('user', 'post_id', 'title', 'medias')
        readonly_fields = ()


class RemarkSerializer(serializers.ModelSerializer):
    """ Get the image url of the user's profile picture """
    """ image_url = serializers.HyperlinkedIdentityField(view_name='<modelname>-detail') """
    user = UserSerializer(many=False)
    created = DateTimeSerializer(many=False)
    
    class Meta:
        model = RemarkModel
        fields = ('user', 'remark_id', 'remark', 'created')


class ReactionSerializer(serializers.ModelSerializer):
    """ get data to be changed, fields that are not being changed should be blank. field being changed to blank should be null """

    user = UserSerializer(many=False)
    created = DateTimeSerializer(many=False)
    
    class Meta:
        model = ReactionModel
        fields = ('user', 'reaction_id', 'reaction', 'created')

