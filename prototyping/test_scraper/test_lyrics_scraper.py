# Import pytest
import pytest

# Test Lyrics Scraper
# Getting Authorization: Bearer Token
import os
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

# Testing if CLIENT_ID and CLIENT_SECRET exist
assert ACCESS_TOKEN != None
#print(f'This is your access_token: {ACCESS_TOKEN}.')

# Importing libraries for scraping
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Import Test CSV
music_data = pd.read_csv('./test_storage/test_music_features.csv')

# Function to Request For Song Information
def request_song_info(track_title, artist):
  search_url = 'https://api.genius.com/search'
  headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
  data_pack = {'q': track_title + ' ' + artist}
  response = requests.get(search_url, data=data_pack, headers=headers)
  return response.json()

# Function to scrape song lyrics based on the URL returned from the function above
def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics

track_lyrics = []
song_name = []

def scrape_lyrics(track_name, artist_name):
  track_lyrics.clear()
  json = request_song_info(track_name, artist_name)
  song_info = None
  for hit in json['response']['hits']:
    if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
      song_info = hit
      break

  # Extract lyrics from URL if the song was found
  if song_info:
    song_url = song_info['result']['url']
    song_name.append(track_name)
    track_lyrics.append(scrap_song_url(song_url))

  else:
    song_name.append(track_name)
    track_lyrics.append('null')

  return track_lyrics[0]

@pytest.mark.parametrize('track_name, artist, expected', [
    ('WANNABE', 'ITZY', 'null'),
    ('TING TING TING with Oliver Heldens', 'ITZY', 'null')
])

def test_run_lyrics(track_name, artist, expected):
  assert scrape_lyrics(track_name, artist) == expected