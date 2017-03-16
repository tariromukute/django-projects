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
from accounts.models import User as UserModel
from fans.models import Fan as FanModel, Request as RequestModel
from fans.serializers import RequestSerializer

# Create your views here.

class Invite(APIView):

    def post(self, request, provider, format=None):

        return Response(status=status.HTTP_201_CREATED)
    
class ListRequests(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    queryset = RequestModel.objects.all()
    # should include serializer_class attribute or overide get_serializer_class() method
    serializer_class = RequestSerializer
    
class Request(APIView):
    
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(user_id=user_id)
        except UserModel.DoesNotExist:
            raise Http404

    def get_object(self, request_id):
        try:
            return UserModel.objects.get(request_id=request_id)
        except UserModel.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        """ count requests """
        number = 1
        return Response(number, status=status.HTTP_200_OK)
    
    def post(self, request, user_id, format=None):
	""" For public accounts no follow request is need """
        user = self.get_object(user_id)
        if user.account_type == 'Public':
            fan = FanModel(
                o_user = user,
                x_user = request.user
            )
            fan.save()
	    """ notify the user that he/she is being followed """

            return Response(status=status.HTTP_201_CREATED)
        """ If account is Private put a follow request """
	    follow = RequestModel(
            o_user = user,
            x_user = request.user
        )
        follow.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    """ respond to follow request """
    def put(self, request, status, request_id, format=None):
        
        follow = self.get_object(request_id)
        if status == 'accept':
            status = 'accepted'
            fan = FanModel(
                o_user = follow.x_user,
                x_user = request.user,
            )
            fan.save()
        else:
            status = 'declined'
        follow.request_status = status
        follow.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, request_id, format=None):

        follow = self.get_object(request_id)
        follow.delete()
        follow.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FanSeen(APIView):

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(user_id=user_id)
        except UserModel.DoesNotExist:
            raise Http404
    
    """ user has seen all new fans """
    def post(self, request, format=None):
        fans = FanModel.objects.get(user=request.user) # filter for those with seen = False
        for x in follows:
            x.seen = True
            x.save()

        return Response(status=status.HTTP_201_CREATED)

    """ user has seen a specific new fan """
    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        fan = FanModel.objects.get(x_user=user) # add requesting user
        fan.seen = True
        fan.save()
        return Response(status=status.HTTP_201_CREATED)


class Tag(APIView):

    def post(self, request, format=None):

        return Response(status=status.HTTP_201_CREATED)
    
