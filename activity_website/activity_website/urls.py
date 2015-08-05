"""activity_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from activity.views import *
from activity_website import settings
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^staticfiles/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS, 'show_indexes': True}),
    #url(r'^$', 'activity.views.home', name = 'home'),
    #url(r'^test/$', 'activity.views.test', name = 'test'),
    url(r'^welcome/$', 'activity.views.welcome', name = 'welcome'),
    url(r'^register/$', 'activity.views.register', name = 'register'),
    url(r'^login/$', 'activity.views.login', name = 'login'),
    url(r'^logout/$', 'activity.views.logout', name = 'logout'),

    url(r'^my_request/$', 'activity.views.my_request', name = 'my_request'),

    url(r'^all_activities/$', 'activity.views.all_activities', name = 'all_activities'),
    url(r'^add_activity/$', 'activity.views.add_activity', name = 'add_activity'),
    url(r'^apply_activity/$', 'activity.views.apply_activity', name = 'apply_activity'),

    url(r'^my_friends/$', 'activity.views.my_friends', name = 'my_friends'),
    url(r'^my_groups/$', 'activity.views.my_groups', name = 'my_groups'),

    url(r'^add_group/$', 'activity.views.add_group', name = 'add_group'),
    url(r'^group/(\d+)/info$', 'activity.views.group_info', name = 'group_info'),
    url(r'^group/(\d+)/members$', 'activity.views.group_members', name = 'group_members'),
    url(r'^group/(\d+)/activities$', 'activity.views.group_activities', name = 'group_activities'),

    url(r'^change_userinfo/$', 'activity.views.change_userinfo', name = 'change_userinfo'),
    url(r'^change_userpwd/$', 'activity.views.change_userpwd', name = 'change_userpwd'),
    url(r'^upload_headimg/$', 'activity.views.upload_headimg', name = 'upload_headimg'),

    url(r'^my_activities/attend/$', 'activity.views.my_activities_attend', name = 'my_activities_attend'),
    url(r'^my_activities/launch/$', 'activity.views.my_activities_launch', name = 'my_activities_launch'),
    url(r'^friend_activities/attend/$', 'activity.views.friend_activities_attend', name = 'friend_activities_attend'),
    url(r'^friend_activities/launch/$', 'activity.views.friend_activities_launch', name = 'friend_activities_launch'),

]

#urlpatterns = patterns('',
#    # existing patterns here...
#    (r'^$', home),
#    (r'^test/$', test),
#    (r'^accounts/login/$',  login),
#    (r'^accounts/logout/$', logout),
#)
