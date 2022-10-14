### So basically I have a playlist that is a complation of all songs in all of my playlists. Before, I had to manually add songs to two playlists when I wanted to save a song - the playlist it belonged to as well as the "Everything" playlist. However, this was annoying so I automated it. Now, running this script will add all songs in other playlists to the "Everything" playlist if the given song is not already in there. 

# Script Descriptions
* syncer.py
    * This script takes all songs from various playlists and adds them to 'Everything', which is a playlist consisting of all unique songs from all playlists. Since spotify added a feature to select multiple playlists when adding songs, it kinda defeats the purpose, but it's still fun to run the script.
* playlist_guesser.py
   * This script (still in development) is aiming to train a classification model so that given a new song, the model can 'predict' which playlist the song belongs in
* playlist_guesser_tester.ipynb
    * Notebook meant for doing some testing before running the playlist_guesser script (because it takes a long time). I can test for bugs with a subset of the dataset and when it works in the tester, I can run the guesser script with the whole dataset.

