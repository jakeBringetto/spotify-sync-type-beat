# Shows a user's playlists (need to be authenticated via oauth)
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def show_tracks(results):
    curr_tracklist = []
    for i, item in enumerate(results['items']):
        track = item['track']
        curr_tracklist.append(track['id'])
    return curr_tracklist
        
if __name__ == '__main__':
    load_dotenv()
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), requests_timeout=10)

    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']
    everything_playlist = [playlist for playlist in playlists['items'] if playlist['name'] == 'Everything'][0]
    results = sp.playlist(everything_playlist['id'], fields="tracks,next")
    tracks = results['tracks']

    tracks_to_exclude = []
    tracks_to_exclude.extend(show_tracks(tracks))
    while tracks['next']:
        tracks = sp.next(tracks)
        tracks_to_exclude.extend(show_tracks(tracks))

    all_track_ids = []
    for playlist in playlists['items']:
        if playlist['name'] != 'Everything':
            if playlist['owner']['id'] == user_id:
                results = sp.playlist(playlist['id'], fields="tracks,next")
                tracks = results['tracks']

                all_track_ids.extend(show_tracks(tracks))
                while tracks['next']:
                    tracks = sp.next(tracks)
                    all_track_ids.extend(show_tracks(tracks))

    all_track_ids = list(set(all_track_ids).difference(set(tracks_to_exclude)))
    print(len(all_track_ids), "songs to add")
    if len(all_track_ids) > 0:
        sp.playlist_add_items(everything_playlist['id'], all_track_ids)



