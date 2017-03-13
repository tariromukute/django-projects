from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

urlpatterns = [
    url(r'^$', views.ListPosts.as_view()),
    url(r'^(?P<post_id>[0-9a-zA-Z]+)/$', views.Post.as_view()), # get: post
    url(r'^remove/(?P<post_id>[0-9a-zA-Z]+)/$', views.Post.as_view()), # delete: post
    url(r'^edit/(?P<post_id>[0-9a-zA-Z]+)/$', views.Post.as_view()), # put: edit post
    url(r'^create/$', views.Post.as_view()), # post: create post
    url(r'^remarks/(?P<post_id>[0-9a-zA-Z]+)/$', views.ListRemarks.as_view()), # get: list of remarks
    url(r'^remark/(?P<post_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # post: create remark
    url(r'^edit/remark/(?P<remark_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # put: edit remark
    url(r'^remove/remark/(?P<remark_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # delete: remove remark
    url(r'^count/remarks/(?P<post_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # get: number of remarks
    url(r'^reactions/(?P<post_id>[0-9a-zA-Z]+)/$', views.ListReactions.as_view()), # get: list of reactions
    url(r'^reaction/(?P<post_id>[0-9a-zA-Z]+)/(?P<reaction_type>[a-z]+)/$', views.Reaction.as_view()), # post: create reation
    url(r'^edit/reaction/(?P<reaction_id>[0-9a-zA-Z]+)/(?P<reaction_type>[a-z]+)/$', views.Reaction.as_view()), # put: change reaction
    url(r'^remove/reaction/(?P<reaction_id>[0-9a-zA-Z]+)/$', views.Reaction.as_view()), # delete: remove reaction
    url(r'^count/reactions/(?P<post_id>[0-9a-zA-Z]+)/$', views.Reaction.as_view()), # get: number of reactions
]

urlpatterns = format_suffix_patterns(urlpatterns)
