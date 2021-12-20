import time
import datetime
import asyncio
import threading
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import Video, YoutubeAPIKey

def str_to_datetime(string):
    splitDateTime = string.split('T')
    return datetime.datetime.strptime(splitDateTime[0] + ' ' + splitDateTime[1].split('Z')[0],'%Y-%m-%d %H:%M:%S')

def update_db(result):
    title = result["snippet"]["title"]
    description = result['snippet']['description']
    channelId = result['snippet']['channelId']
    thumbnails = result['snippet']['thumbnails']['default']['url']
    publishedAt = str_to_datetime(result['snippet']['publishedAt'])

    video_obj = Video(title=title, description=description, channelId=channelId, thumbnails=thumbnails, publishedAt=publishedAt)
    video_obj.save()


def client_conect(key):
    QUERY = "football"
    MAX_RESULTS = 50
    publishedAfter = datetime.datetime(2021, 12, 1).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        youtube = build("youtube", "v3", developerKey=key.key)
        search_exec = youtube.search().list(type='video', order='date', q=QUERY, part="id, snippet", maxResults=MAX_RESULTS, publishedAfter=publishedAfter).execute()
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

        try:
            latest_video_db = Video.objects.all().order_by('-publishedAt').first()
            latest_video_publishedAt_db = latest_video_db.publishedAt
        except:
            latest_video_publishedAt_db = datetime.datetime.min 

        
        for result in data:
            publishedAt = str_to_datetime(result['snippet']['publishedAt'])
            if(publishedAt > latest_video_publishedAt_db):
                update_db(result)


        await asyncio.sleep(300) # Sleep for 5 minutes


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