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
from accounts.serializers import RegisterSerializer, UserSerializer, UserIDSerializer, ExtendedUserSerializer, EditUserSerializer
from accounts.models import User as UserModel
from medias.models import Media as MediaModel

# Create your views here.

# Register the user into the system
class Register(APIView):

    def create(self, data):
        user = UserModel(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
        )
        user.set_password(data['password'])
        user.save()
        return user
    
    def generate_code(self, size=10, chars=string.ascii_uppercase + string.digits):

        return ''.join(random.choice(chars) for i in range(size))
        
    """ insert user details and send email with code """
    def post(self, request, format=None):
        user=self.create(request.data)
        user.code = self.generate_code()
        user.save()
            #user.email_user("Account Verification", settings.SITE_URL+"/"+user.user_id+"/"+user.code+"/")
        serializer = UserIDSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Verify email and activate user
class VerifyEmail(APIView):

    def get_object(self, user_id):
        try:
            return UserModel.objects.get(user_id=user_id)
        except UserModel.DoesNotExist:
            raise Http404

    def get(self, request, user_id, code, format=None):
        user = self.get_object(user_id)
        if user.code != code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_201_CREATED)
"""
    def get(self, request, user_id, code, format=None):
        
        user = self.get_object(user_id)
        verify code 
        if user.code != code:
             return bad request if invalid code 
            return Response(status=status.HTTP_400_BAD_REQUEST)
            set is_active=True and return created if code is valid 
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_204_CREATED)
"""
class User(APIView):

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    
    def get_object(self, user_id):
        try:
            return UserModel.objects.get(user_id=user_id)
        except UserModel.DoesNotExist:
            raise Http404

    """ retrieve user details """
    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    """ edit user details """
    def put(self, request, user_id, format=None):
        user = request.user
        serializer = EditUserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExtendedUser(APIView):

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    
    def get_object(self, user_id):
        try:
            return UserModel.objects.get(user_id=user_id)
        except user.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = ExtendedUserSerializer(user)
        return Response(serializer.data)
        

class DisplayPicture(APIView):

    def get_object(self, media_id):
        try:
            return MediaModel.objects.get(media_id=media_id)
        except MediaModel.DoesNotExist:
            return Http404

    def put(self, request, media_id, format=None):
        media = self.get_object(media_id)
        request.user.display_picture = media
        request.user.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        request.user.diplay_picture = None #None not work, set a media that has the image of no pp instead
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
