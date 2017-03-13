from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from notifications import views

urlpatterns = [
    url(r'^$', views.ListNotifications.as_view()),
    url(r'^remove/(?P<notification_id>[0-9a-zA-Z]+)/$', views.Notification.as_view()), # delete: notification
    url(r'^count/notifications/$', views.Notification.as_view()), # get: number of not seen notifications
    url(r'^seen/(?P<notification_id>[0-9a-zA-Z]+)/$', views.Notification.as_view()), # put: notification seen
]

urlpatterns = format_suffix_patterns(urlpatterns)
