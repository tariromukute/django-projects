import datetime
from rest_framework import serializers
from fans.models import Request as RequestModel
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
        
    
class RequestSerializer(serializers.ModelSerializer):

    created = DateTimeSerializer(many=False)
    x_user = UserSerializer(many=False)
    
    class Meta:
        model = RequestModel
        fields = ('x_user', 'created')
        readonly_fields = ()
