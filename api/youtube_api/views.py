from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination

from .models import Video
from .serializers import VideoSerializer, YoutubeAPIKeySerializer

class VideosListAPI(generics.ListAPIView):
    """
    API for getting list of all the videos, order by latest published time.
    """
    queryset = Video.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
   
    # Adding the search and filter fields
    search_fields = ['title']
    filter_fields = ['channelTitle']

    ordering = ['-publishedAt'] # Sorting the videos in reverse chronological of publish date time

    serializer_class = VideoSerializer