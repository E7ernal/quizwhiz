# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.conf.urls import url

from quizard import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^about/$', views.About.as_view(), name='about'),
    url(r'^assignment/(?P<code>\w+)/$', views.Assignment.as_view(), name='assignment'),
    url(r'^assignment/(?P<code>\w+)/question/(?P<question_slug>[\w_-]+)/$', views.Question.as_view(), name='question'),
    url(r'^assignment/(?P<code>\w+)/results/$', views.Results.as_view(), name='results'),
    url(r'^assignments/(?P<school>[\w_-]+)/(?P<teacher>\w+)/$', views.AssignmentList.as_view(), name='assignments'),
]
