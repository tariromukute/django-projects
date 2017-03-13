from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = [
    url(r'^register/$', views.Register.as_view()), # post: register user
    url(r'^verify/(?P<user_id>[0-9a-zA-Z]+)/(?P<code>[0-9a-zA-Z]+)/$', views.VerifyEmail.as_view()), # get: verify user's email
    url(r'^user/(?P<user_id>[0-9a-zA-Z]+)/$', views.User.as_view()), # get: user details
    url(r'^user/edit/$', views.User.as_view()), # put: edit user details
    url(r'^user/details/(?P<user_id>[0-9a-zA-Z]+)/$', views.ExtendedUser.as_view()), # get: extended user details
    url(r'^user/display_picture/(?P<media_id>[0-9a-zA-Z]+)/$', views.DisplayPicture.as_view()), # put: user dp
    url(r'^user/display_picture/$', views.DisplayPicture.as_view()), # delete: user's dp
]

urlpatterns = format_suffix_patterns(urlpatterns)
