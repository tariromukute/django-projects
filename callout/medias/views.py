from django.shortcuts import render
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from accounts.permissions import IsOwnerOrReadOnly
from medias.models import Media

# Create your views here.

class UploadMedia(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        if 'media' in request.data:
            upload = request.data['media']
            media = Media(user=request.user)
            media.media_url.save(upload.name, upload)
            media.save()

            return Response(media.media_id, status=status.HTTP_201_CREATED, headers={'Location': media.media_url})    
        return Response(status=status.HTTP_400_BAD_REQUEST)

