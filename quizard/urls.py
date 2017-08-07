# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.conf.urls import url

from quizard import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^assignment/(?P<code>\w+)/?', views.Assignment.as_view(), name='assignment'),
    url(r'^assignments/(?P<school>[\w\s]+)/(?P<teacher>\w+)/?$', views.AssignmentList.as_view(), name='assignments'),
]
