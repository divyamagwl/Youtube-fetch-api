from django.urls import path

from .views import VideosListAPI, AddYoutubeKeyAPI
from .services import THREAD

urlpatterns = [
	path('videos', VideosListAPI.as_view(), name="Videos"),
	path('addYoutubeKey', AddYoutubeKeyAPI.as_view()),
]

THREAD.start()