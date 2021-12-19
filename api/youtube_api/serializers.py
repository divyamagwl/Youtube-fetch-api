from rest_framework import serializers

from .models import Video, YoutubeAPIKey

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for Video Model
    """
    class Meta:
        model = Video
        fields = '__all__'

class YoutubeAPIKeySerializer(serializers.ModelSerializer):
    """
    Serializer for APIKey Model.
    """
    class Meta:
        model = YoutubeAPIKey
        fields = '__all__'