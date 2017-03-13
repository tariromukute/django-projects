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
from callouts.models import Callout as CalloutModel, Remark as RemarkModel, Reaction as ReactionModel, OPost as OPostModel
from posts.models import Post as PostModel
from callouts.serializers import CalloutSerializer, RemarkSerializer, ReactionSerializer
# Create your views here.

class ListCallouts(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    queryset = CalloutModel.objects.all()
    # should include serializer_class attribute or overide get_serializer_class() method
    serializer_class = CalloutSerializer
    
class Callout(APIView):

    def get_object(self, callout_id):
        try:
            return CalloutModel.objects.get(callout_id=callout_id)
        except CalloutModel.DoesNotExist:
            raise Http404

    def get_post(self, post_id):
        try:
            return PostModel.objects.get(post_id=post_id)
        except PostModel.DoesNotExist:
            raise Http404

    def get(self, request, callout_id, format=None):
        callout = self.get_object(callout_id)
        selializer = CalloutSerializer(callout)
        return Response(serializer.data)
    
    """ challenge posts """
    def post(self, request, format=None):
        callout = CalloutModel(
            user = request.user,
            pub_date = request.data['pub_date'],
        )
        opost_list = None
        notification_list = None
        for x in request.data['o_posts']:
            opost_list.add(OPostModel(
                callout = callout,
                post = get_post(x)
                )
            )
            notification_list.add(NotificationModel(
                o_user = post.user,
                x_user = request.user,
                type_id = callout.callout_id,
                notification_type = 'Callout_Challenge',
                )
            )

        """ save entity, separated to ensure taht they are only saved if all post_id are found """
        i = 0
        for x in opost_list:
            x.save()
            notification_list[i].save()
            i =i+1
            
        callout.save()

        """ generate notification """
        
        """ carry the whose create """
        return Response(callout.callout_id)


    def put(self, request, callout_id, format=None):
        callout = self.get_object(callout_id)
        if callout.user is not request.user:
            return Response(status=status.HTTP_403_FORBBIDEN)

        """ do all the updates """
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, callout_id, format=None):
        callout = self.get_object(callout_id)
        callout.delete()
        callout.save()
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
        
    """ get remark number of remarks """
    def get(self, request, callout_id, format=None):
        """ count remarks """
        return Response(serializer.data)

    def post(self, request, callout_id, format=None):
        callout = CalloutModel.objects.get(callout_id=callout_id)
        remark = RemarkModel(
           user = request.user,
           callout = callout,
           remark = request.data['remark'],
           remark_type = request.data['remark_type'],
        )
        remark.save()
        """
        user_list = CalloutModel.objects.get() # user with opost
        for x in user_list:            
            notification = NotificationModel(
                o_user = x,
                x_user = request.user,
                type_id = remark.remark_id,
                notification_type = 'callout_remark',
            )
            notification.save()
        """
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
    def get(self, request, format=None):
        """ count reactions """
        return Response(serializer.data)

    def post(self, request, o_post_id, reaction_type, format=None):
        opost = OPostModel.objects.get(o_post_id=o_post_id)
        reaction = RemarkModel(
           user = request.user,
           opost = opost,
           reaction = reaction_type,
        )
        reaction.save()
        notification = NotificationModel(
            o_user = opost.post.user,
            x_user = request.user,
            type_id = opost.callout.callout_id,
            notification_type = 'callout_reaction',
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
        

class OPost(APIView):

    def get_object(self, o_post_id):
        try:
            return OPostModel.objects.get(o_post_id=o_post_id)
        except OPostModel.DoesNotExist:
            raise Http404
        
    """ accept/decline challenge """    
    def put(self, request, status, o_post_id, format=None):
        opost = self.get_object(o_post_id)
        opost.post_status = status
        opost.save()

        if status == 'accept':
            status = 'callout_challenge_accepted'
        else:
            status = 'callout_challenge_declined'
            
        notification = NotificationModel(
            o_user = opost.callout.user,
            x_user = request.user,
            type_id = opost.callout.callout_id,
            notification_type = status,
        )
        notification.save()
        return Response(status=status.HTTP_201_CREATED)

    
