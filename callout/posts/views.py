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
from accounts.models import User as UserModel
from medias.models import Media as MediaModel
from posts.models import Post as PostModel, Remark as RemarkModel, Reaction as ReactionModel
from posts.serializers import PostSerializer, RemarkSerializer, ReactionSerializer
# Create your views here.

""" get list of remarks """
class ListPosts(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    queryset = PostModel.objects.all()
    # should include serializer_class attribute or overide get_serializer_class() method
    serializer_class = PostSerializer
    
class Post(APIView):

    def get_object(self, post_id):
        try:
            return PostModel.objects.get(post_id=post_id)
        except PostModel.DoesNotExist:
            raise Http404
        
    def get_media(self, media_id):
        try:
            return MediaModel.objects.get(media_id=media_id)
        except MediaModel.DoesNotExist:
            raise Http404

    def get(self, request, post_id, format=None):
        post = self.get_object(post_id)
        selializer = PostSerializer(post)
        return Response(serializer.data)
    
    """ create post """
    def post(self, request, format=None):
        for x in request.data['media_ids']:
            if self.get_media(x).user is not request.user:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        """ carry the whose create """
        return Response(post.post_id)


    def put(self, request, post_id, format=None):
        post = self.get_object(post_id)
        if post.user is not request.user:
            return Response(status=status.HTTP_403_FORBBIDEN)

        """ do all the updates """
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, post_id, format=None):
        post = self.get_object(post_id)
        post.delete()
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

""" get list of remarks """
class ListRemarks(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    queryset = RemarkModel.objects.all()
    # should include serializer_class attribute or overide get_serializer_class() method
    serializer_class = RemarkSerializer

class Remark(APIView):

    def get_object(self, remark_id):
        try:
            return RemarkModel.objects.get(remark_id=remark_id)
        except RemarkModel.DoesNotExist:
            raise Http404
        
    """ get number of post remarks """
    def get(self, request, post_id, format=None):
        """ count remarks """
        serializer = RemarkSerializer(remark)
        return Response(serializer.data)

    def post(self, request, post_id, format=None):
        post = PostModel.objects.get(post_id=post_id)
        remark = RemarkModel(
           user = request.user,
           post = post,
           remark = request.data['remark'],
           remark_type = request.data['remark_type'],
        )
        remark.save()
        notification = NotificationModel(
            o_user = post.user,
            x_user = request.user,
            type_id = post.post_id,
            notification_type = 'post_remark',
        )
        notification.save()
        return Response(remark.remark_id)

    def put(self, request, remark_id, format=None):
        remark = self.get_object(remark_id)
        remark.remark = request.data['remark']
        remark.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, remark_id, format=None):
        remark = self.get_object(remark_id)
        remark.delete()
        remark.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" get list of remarks """
class ListReactions(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    queryset = ReactionModel.objects.all()
    # should include serializer_class attribute or overide get_serializer_class() method
    serializer_class = ReactionSerializer


class Reaction(APIView):

    def get_object(self, reaction_id):
        try:
            return ReactionModel.objects.get(reaction_id=reaction_id)
        except ReactionModel.DoesNotExist:
            raise Http404

    """ get reaction with the reaction_id """
    def get(self, request, reaction_id, format=None):
        """ count reactions """
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)

    def post(self, request, post_id, reaction_type, format=None):
        post = PostModel.objects.get(post_id=post_id)
        reaction = RemarkModel(
           user = request.user,
           post = post,
           reaction = reaction_type,
        )
        reaction.save()
        notification = NotificationModel(
            o_user = post.user,
            x_user = request.user,
            type_id = post.post_id,
            notification_type = 'post_reaction',
        )
        notification.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, reaction_id, reaction_type, format=None):
        reaction = self.get_object(reaction_id)
        reaction.reaction = reaction_type
        reaction.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, reaction_id, format=None):
        reaction = self.get_object(reaction_id)
        reaction.delete()
        reaction.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

