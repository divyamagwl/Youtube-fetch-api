import time
import datetime
import asyncio
import threading
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import Video, YoutubeAPIKey


def str_to_datetime(string):
    splitDateTime = string.split('T')
    return datetime.datetime.strptime(
        splitDateTime[0] + ' ' + splitDateTime[1].split('Z')[0], '%Y-%m-%d %H:%M:%S'
    )


def update_db(result):
    video_id = result["id"]["videoId"]
    title = result["snippet"]["title"]
    description = result['snippet']['description']
    publishedAt = str_to_datetime(result['snippet']['publishedAt'])
    thumbnail = result['snippet']['thumbnails']['default']['url']
    channel_title = result["snippet"]["channelTitle"]
    channelId = result['snippet']['channelId']

    video_obj = Video(
        videoId=video_id,
        title=title,
        description=description,
        publishedAt=publishedAt,
        thumbnail=thumbnail,
        channelId=channelId,
        channelTitle=channel_title
    )
    video_obj.save()


def client_conect(key):
    QUERY = "football"
    MAX_RESULTS = 50
    publishedAfter = datetime.datetime(2021, 12, 1).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        youtube = build("youtube", "v3", developerKey=key.key)
        search_exec = (
            youtube.search()
            .list(
                type='video',
                order='date',
                q=QUERY,
                part="id, snippet",
                maxResults=MAX_RESULTS,
                publishedAfter=publishedAfter,
            )
            .execute()
        )
        results = search_exec.get("items", [])
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n {e.content}')
        key.quotaFinished = False
        key.save()
        return {}

    return results


async def fetch_videos(key):
    while True:
        data = client_conect(key)

        if data == {}:
            return

        for result in data:
            # Only unique entries will be saved. Uniqueness is identified using video_id from youtube.com
            try:
                update_db(result)
            except Exception as e:
                print(e)
                continue

        await asyncio.sleep(300)

# Schedule searching for new youtube videos
def scheduled_searching():
    while True:
        api_keys = YoutubeAPIKey.objects.filter(quotaFinished=False)

        # All keys have finished their quota
        if not len(api_keys):
            return

        key = api_keys[0]
        asyncio.run(fetch_videos(key))

        time.sleep(10)


THREAD = threading.Thread(target=scheduled_searching)
