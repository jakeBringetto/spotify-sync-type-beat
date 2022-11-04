# Shows a user's playlists (need to be authenticated via oauth)
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import sys
import playlist_guesser_data_extractor as pl
from numpy import loadtxt
import csv
from sklearn.ensemble import RandomForestClassifier

def get_data():
    all_track_data = loadtxt('data.csv', delimiter=',')
    all_track_labels = []
    with open('labels.csv', newline='') as csvfile:
        label_reader = csv.reader(csvfile, delimiter=',')
        for row in label_reader:
            for label in row:
                all_track_labels.append(label[2:-2])
    all_track_labels = np.array([all_track_labels]).T
    return all_track_data, all_track_labels

def get_tracks():
    final_tracks = []
    final_track_features = []
    for playlist in playlists['items']:
        name = playlist['name']
        if name == "Bot Test" and playlist['owner']['id'] == user_id:
            results = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']

            track_features = []
            track_features.extend(pl.extract_track_features(sp, tracks))
            while tracks['next']:
                tracks = sp.next(tracks)
                track_features.extend(pl.extract_track_features(sp, tracks))

            track_data = []
            for track in track_features:
                data = pl.formulate_feature_data(track)
                if data:
                    track_data.append(data)
                    final_tracks.append(track)
            if len(track_data) > 0:
                final_track_features.extend(track_data)
    final_tracks = [sp.track(track['id'])['name'] for track in final_tracks]
    return final_tracks, np.array(final_track_features)


if __name__ == '__main__':
    load_dotenv()
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']

    if len(sys.argv) > 1 and sys.argv[1] == 'extract':
        pl.extract()

    all_track_data, all_track_labels = get_data()
    depth = 10
    estimators = 100
    model = RandomForestClassifier(max_depth=depth, n_estimators=estimators, criterion='entropy', max_features='sqrt')
    model.fit(all_track_data, np.ravel(all_track_labels))
    tracks, track_features = get_tracks()
    track_predictions = model.predict(track_features)
    for i in range(len(tracks)):
        print("Track:", tracks[i], "Prediction:", track_predictions[i])