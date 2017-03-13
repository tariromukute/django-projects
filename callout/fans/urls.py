from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from fans import views

""" should add invite urls """
urlpatterns = [
    url(r'^$', views.ListRequests.as_view()),
    url(r'^remove/request/(?P<request_id>[0-9a-zA-Z]+)/$', views.Request.as_view()), # delete: request
    url(r'^count/requests/$', views.Request.as_view()), # get: number of not seen requests
    url(r'^request/(?P<user_id>[0-9a-zA-Z]+)/$', views.Request.as_view()), # put: make a fan request
    url(r'^request/(?P<status>[a-z]+)/(?P<request_id>[0-9a-zA-Z]+)/$', views.Request.as_view()), # put: request status
    url(r'^seen/$', views.FanSeen.as_view()), # put: set seen=True for that fan user only
    url(r'^seen/(?P<user_id>[0-9a-zA-Z]+)/$', views.FanSeen.as_view()), # post: sets seen=True for all seen=False
]

urlpatterns = format_suffix_patterns(urlpatterns)
