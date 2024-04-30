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

def get_playlist_ids(username,playlist_id):
    r = sp.user_playlist_tracks(username,playlist_id)
    t = r['items']
    ids = []
    while r['next']:
        r = sp.next(r)
        t.extend(r['items'])
    for s in t: ids.append(s["track"]["id"])
    return ids
        
if __name__ == '__main__':
    load_dotenv()
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), requests_timeout=10)

    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']
    everything_playlist = [playlist for playlist in playlists['items'] if playlist['name'] == 'Everything'][0]
    tracks_to_exclude = get_playlist_ids(user_id, everything_playlist['id'])

    all_track_ids = []
    for playlist in playlists['items']:
        if playlist['name'] != 'Everything':
            if playlist['owner']['id'] == user_id:
                tracks = get_playlist_ids(user_id, playlist['id'])
                all_track_ids.extend(tracks)
    all_track_ids = list(set(all_track_ids).difference(set(tracks_to_exclude)))
    print(len(all_track_ids), "songs to add")
    if len(all_track_ids) > 0:
        i = 0
        while i < len(all_track_ids):
            sp.playlist_add_items(everything_playlist['id'], all_track_ids[i:i+50])
            i += 50



