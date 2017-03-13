from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from callouts import views

urlpatterns = [
    url(r'^$', views.ListCallouts.as_view()),
    url(r'^(?P<callout_id>[0-9a-zA-Z]+)/$', views.Callout.as_view()), # get: callout
    url(r'^remove/(?P<callout_id>[0-9a-zA-Z]+)/$', views.Callout.as_view()), # delete: callout
    url(r'^edit/(?P<callout_id>[0-9a-zA-Z]+)/$', views.Callout.as_view()), # put: edit callout
    url(r'^challenge/$', views.Callout.as_view()), # post: challenge list of posts
    url(r'^remarks/(?P<callout_id>[0-9a-zA-Z]+)/$', views.ListRemarks.as_view()), # get: list of remarks
    url(r'^remark/(?P<callout_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # post: create remark
    url(r'^edit/remark/(?P<remark_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # put: edit remark
    url(r'^remove/remark/(?P<remark_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # delete: remove remark
    url(r'^count/remarks/(?P<callout_id>[0-9a-zA-Z]+)/$', views.Remark.as_view()), # get: number of remarks
    url(r'^reactions/(?P<callout_id>[0-9a-zA-Z]+)/$', views.ListReactions.as_view()), # get: list of reactions
    url(r'^reaction/(?P<callout_id>[0-9a-zA-Z]+)/(?P<reaction_type>[a-z]+)/$', views.Reaction.as_view()), # post: create reation
    url(r'^edit/reaction/(?P<reaction_id>[0-9a-zA-Z]+)/(?P<reaction_type>[a-z]+)/$', views.Reaction.as_view()), # put: change reaction
    url(r'^remove/reaction/(?P<reaction_id>[0-9a-zA-Z]+)/$', views.Reaction.as_view()), # delete: remove reaction
    url(r'^count/reactions/(?P<callout_id>[0-9a-zA-Z]+)/$', views.Reaction.as_view()), # get: number of reactions
    url(r'^challenge/(?P<status>[0-9a-z]+)/(?P<o_post_id>[0-9a-zA-Z]+)/$', views.OPost.as_view()), # put: accept/decline challenge
]

urlpatterns = format_suffix_patterns(urlpatterns)
