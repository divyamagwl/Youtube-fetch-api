<h1 align="center">Youtube Fetch API</h1>

![Django Version](https://img.shields.io/badge/Django-4.0.0-brightgreen) ![Django Rest](https://img.shields.io/badge/Django%20rest%20framework-3.13.1-brightgreen)

## Installation

	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	cd api
	python3 manage.py migrate

## Runnning the server

	python3 manage.py runserver

## About the project

This project was created as part of the FamPay Backend assignment.

### Project Aim
An API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

### Implementation Details:
<ul>
<li> Server calls the YouTube API continuously in background (async) with a interval of 5 minutes for fetching the latest videos for predefined search query "football". Then it stores the data of videos in a database with proper indexes.

<li> A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.

<li> Added support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.

<li> Optimized to store only unique videos in the database.

</ul>


## API Documentation:
-----------------

i. Get Videos

API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for "youtube" query in a paginated response.

	Endpoint 	: /videos


ii. Add Youtube API Key

API for adding a new Youtube Data API Key in the database. 

	Endpoint	: /addYoutubeKey

## How to use the API:

1. Direct to /addYoutubeKey and add one youtube data api key. You can read [here](https://developers.google.com/youtube/v3/getting-started) on how to get the api key.

2. Redirect to /videos to see the videos fetched by the server. 

3. Wait 5 mins to get new videos if there are any.

## Tech Stack

1. Python <br>
2. Django <br>
3. SQLite <br>


## Show your support

Give a ⭐️ if you like the project!
