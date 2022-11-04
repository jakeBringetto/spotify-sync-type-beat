# Shows a user's playlists (need to be authenticated via oauth)
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import sys
import playlist_guesser_data_extractor

def extract_track_features(results):
    curr_tracklist = []
    for i, item in enumerate(results['items']):
        track = item['track']
        if track:
            curr_tracklist.append(sp.audio_features(track['uri'])[0])
    return curr_tracklist

def formulate_feature_data(track):
    if track:
        acousticness = track['acousticness']
        danceability = track['danceability']
        energy = track['energy']
        key = track['key']
        loudness = track['loudness']
        speechiness = track['speechiness']
        instrumentalness = track['instrumentalness']
        liveness = track['liveness']
        valence = track['valence']
        tempo = track['tempo']

        track_data = [acousticness, danceability, energy, key, loudness, 
        speechiness, instrumentalness, liveness, valence, tempo]

        return track_data
    else:
        return None

if __name__ == '__main__':
    load_dotenv()
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    if len(sys.argv) > 1 and sys.argv[1] == 'extract':
        playlist_guesser_data_extractor.extract()
    
