# Shows a user's playlists (need to be authenticated via oauth)
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

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
    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']

    all_track_data = []
    for playlist in playlists['items']:
        name = playlist['name']

        results = sp.playlist(playlist['id'], fields="tracks,next")
        tracks = results['tracks']

        track_features = []
        track_features.extend(extract_track_features(tracks))
        while tracks['next']:
            tracks = sp.next(tracks)
            track_features.extend(extract_track_features(tracks))

        track_data = []
        for track in track_features:
            data = formulate_feature_data(track)
            if data:
                track_data.append(data)
        if len(track_data) > 0:
            all_track_data.extend(track_data)

    all_track_data = np.array(all_track_data)
    print(all_track_data.shape())
    
