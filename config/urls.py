"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from rest_framework import routers

from ingeupdong.views import TrendingViewSet, RecordingViewSet, ChannelViewSet, VideoViewSet,\
    ChannelListView
from rank.views import Ranking

router = routers.DefaultRouter()
router.register(r'trending', TrendingViewSet, basename='trend')
router.register(r'recording', RecordingViewSet, basename='record')
router.register(r'channel', ChannelViewSet, basename='channel')
router.register(r'video', VideoViewSet, basename='video')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/search/', ChannelListView.as_view()),
    path('api/rank/', Ranking.as_view()),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
