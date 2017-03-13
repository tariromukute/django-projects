from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from medias import views

urlpatterns = [
    url(r'^upload/$', views.UploadMedia.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
