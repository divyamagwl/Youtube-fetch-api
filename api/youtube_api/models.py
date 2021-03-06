from django.db import models


class Video(models.Model):
    videoId = models.CharField(max_length=100, unique=True) # Unique id of the video
    title = models.CharField(max_length=255)  # Title of the video
    description = models.CharField(max_length=1000)  # Description of the video
    publishedAt = models.DateTimeField()  # Publish date time Of the video
    thumbnail = models.URLField()  # URL Of the video thumbnails
    channelId = models.CharField(max_length=100)  # Id Of the channel
    channelTitle = models.CharField(max_length=200) # Name of the channel

    def __str__(self):
        return self.title


class YoutubeAPIKey(models.Model):
    key = models.TextField()
    quotaFinished = models.BooleanField(default=False)
