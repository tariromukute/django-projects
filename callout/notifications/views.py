import string
import random
from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from accounts.permissions import IsOwnerOrReadOnly
from fans.permissions import PeerAccess
from notifications.models import Notification as NotificationModel
from notifications.serializers import NotificationSerializer

# Create your views here.

class ListNotifications(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    queryset = NotificationModel.objects.all()
    # should include serializer_class attribute or overide get_serializer_class() method
    serializer_class = NotificationSerializer

class Notification(APIView):

    def get_object(self, notification_id):
        try:
            return NotificationModel.objects.get(notification_id=notification_id)
        except NotificationModel.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        """ count notifications """
        number = 1
        return Response(number, status=status.HTTP_200_SUCCESS)

    def put(self, request, notification_id, format=None):
        notification = self.get_object(notification_id)
        notification.seen = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, notification_id, format=None):

        notification = self.get_object(notification_id)
        notification.delete()
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
