import datetime
from rest_framework import serializers
from notifications.models import Notification as NotificationModel
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
        
    
class NotificationSerializer(serializers.ModelSerializer):

    created = DateTimeSerializer(many=False)
    x_user = UserSerializer(many=False)
    
    class Meta:
        model = NotificationModel
        fields = ('x_user', 'notification_id', 'notification_type', 'type_id', 'seen', 'created')
        readonly_fields = ()
