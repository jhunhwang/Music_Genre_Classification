# Getting Client ID and Client Secret
import os
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

# Testing if CLIENT_ID and CLIENT_SECRET exist
assert CLIENT_ID != None; assert CLIENT_SECRET != None
print(f'This is your client_id: {CLIENT_ID}.\nThis is your client_secret: {CLIENT_SECRET}.')

# Importing libraries for scraping
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Import Data Dict Pack
import data_dict
music_info = data_dict.music_data

# Spotify API Login
CLIENT_CREDENTIALS = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS)

# Artist Input (ITZY For Sample) (sample.txt)
artist_name = []
with open('./sample_artist_list/sample_input.txt') as sample:
    for name in sample:
        artist_name.append(str(name.strip()))

# Feature Names
feature_list = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'isWestern']
temp_loop_feature = feature_list[:-1]

# Append the artists that were entered by the user in the ``artist_name`` list.
for i in artist_name:
    music_info['call_data']['kpop_western'].append(i)

# Loop through all the artists
for artist_name in music_info['call_data']['kpop_western']:

    result = sp.search(artist_name, type='artist', limit=1)

    artist_uri = result['artists']['items'][0]['uri']

    artist_genre = result['artists']['items'][0]['genres']

    sp_albums = sp.artist_albums(artist_uri, album_type='album')

    sp_single_ep = sp.artist_albums(artist_uri, album_type='single')

    sp_albums_sep_uri_temp = [sp_albums['items'][i]['uri'] for i in range(len(sp_albums["items"]))] + [sp_single_ep['items'][j]['uri'] for j in range(len(sp_single_ep['items']))]

    sp_albums_sep_name_temp = [sp_albums['items'][i]['name'] for i in range(len(sp_albums['items']))] + [sp_single_ep['items'][j]['name'] for j in range(len(sp_single_ep['items']))]

    sp_track_uri_temp = []

    for x, y in zip(sp_albums_sep_uri_temp, sp_albums_sep_name_temp):

        print(x, y)

        for j in range(len(sp.album_tracks(x)['items'])):

            print(len(sp.album_tracks(x)['items']))

            music_info['song_dtl']['album_name'].append(y)

            music_info['song_dtl']['album_uri'].append(x)

            sp_track_uri_temp.append(sp.album_tracks(x)['items'][j]['uri'])

            music_info['song_dtl']['track_uri'].append(sp.album_tracks(x)['items'][j]['uri'])

            music_info['song_dtl']['track_name'].append(sp.album_tracks(x)['items'][j]['name'])

    for track in sp_track_uri_temp:

        track_af = sp.audio_features(tracks=track)

        print(track_af)

        try:

            for feature in temp_loop_feature:

                music_info['song_ftr'][feature].append(track_af[0][feature])
            
            track_pop = sp.track(track)

            music_info['song_ftr']['popularity'].append(track_pop['popularity'])
        except:

            for feature in feature_list:

                music_info['song_ftr'][feature].append('null')

            continue

    for i in range(len(sp_track_uri_temp)):

        music_info['song_dtl']['artist_name'].append(artist_name)

        music_info['song_dtl']['artist_uri'].append(artist_uri)

        music_info['song_dtl']['artist_genre'].append(artist_genre)

# Added as I went along (Always looking for better solutions)
# To do list (Separate K-Pop and other genres so that the list above can be used.)
kpop = ['ITZY', 'DREAMCATCHER', 'BLACKPINK', 'TWICE', 'Red Velvet', 'BTS', 'EXO', 'Wanna One', 'Got7', 'SEVENTEEN', 'Monsta X', 'Stray Kids']
western = ['Chainsmokers', 'The Weeknd', 'Taylor Swift', 'Ariana Grande', 'Sam Smith', 'Justin Bieber', 'Lauv', 'One Direction', 'Harry Styles', 'Lizzo', 'Ed Sheeran', 'Justin Timberlake']

for i in music_info['song_dtl']['artist_name']:

    if i in kpop:
        music_info['ml_classification']['isWestern'].append(0)
 
    elif i in western:
        music_info['ml_classification']['isWestern'].append(1)

song_df = pd.DataFrame({'artist': music_info['song_dtl']['artist_name'],
                        'artist_uri': music_info['song_dtl']['artist_uri'], 
                        'artist_genre': music_info['song_dtl']['artist_genre'],
                        'album_name': music_info['song_dtl']['album_name'],
                        'album_uri': music_info['song_dtl']['album_uri'], 
                        'track_name': music_info['song_dtl']['track_name'], 
                        'track_uri': music_info['song_dtl']['track_uri'], 
                        'danceability': music_info['song_ftr']['danceability'], 
                        'energy': music_info['song_ftr']['energy'], 
                        'key': music_info['song_ftr']['key'], 
                        'loudness': music_info['song_ftr']['loudness'], 
                        'mode': music_info['song_ftr']['mode'], 
                        'speechiness': music_info['song_ftr']['speechiness'], 
                        'acousticness': music_info['song_ftr']['acousticness'], 
                        'instrumentalness': music_info['song_ftr']['instrumentalness'], 
                        'liveness': music_info['song_ftr']['liveness'], 
                        'valence': music_info['song_ftr']['valence'], 
                        'tempo': music_info['song_ftr']['tempo'], 
                        'duration_ms': music_info['song_ftr']['duration_ms'], 
                        'popularity': music_info['song_ftr']['popularity'],
                        'time_signature': music_info['song_ftr']['time_signature'], 
                        'isWestern': music_info['ml_classification']['isWestern']})

song_df = song_df.drop_duplicates(subset=['track_name', 'duration_ms', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'], keep='first')

song_df.to_csv('./test_storage/test_music_features.csv', index=False)

print(song_df)