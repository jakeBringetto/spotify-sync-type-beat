
# Script Descriptions
* `syncer.py`
    * This script takes all songs from various playlists and adds them to 'Everything', which is a playlist consisting of all unique songs from all playlists. Since spotify added a feature to select multiple playlists when adding songs, it kinda defeats the purpose, but it's still fun to run the script.
* `playlist_guesser.py`
   * This script (still in development) is aiming to train a classification model so that given a new song, the model can 'predict' which playlist the song belongs in. This particular classifier is a random forest.
* `playlist_guesser_tester.ipynb`
    * Notebook meant for doing some testing before running the `playlist_guesser` script (because it takes a long time). I can test for bugs with a subset of the dataset and when it works in the tester, I can run the guesser script with the whole dataset.
    * Currently working on hyperparameter tuning for the random forest.
    * Next steps include trying out other classification architectures. 
    * I also would like to create new features and potentially implement an autoencoder model to get a latent form of my song vectors to take advantage of larger datasets.
* `extractor.py`
     * Fetching the data and labels takes quite a long time, so I have a script for fetching and putting the data/labels into csv files called `data.csv` and `label.csv`. I can then read from the csv files when I want to use the data/labels, which is must faster than extracting and creating the arrays everytime.

# Running the code
### Syncing
Simply run `python3 syncer.py` in the directory with the file. It will open a prompt in your browser to allow permission to access spotify user data.

### Guessing
Run `python3 extractor.py` to create and store data/label arrays.

Then, run `python3 playlist_guesser.py <model>` to guess playlist for song, where model is one of {`dt`}

Additionally, to avoid having to run two scripts, run `python3 playlist_guesser_dt.py model extract` to first extract then predict.

# Future work (to do)
As of now the code is essentially only able to run with my settings. I will make it more accessible in the future. At the moment, anyone wanting to use the code needs to have their own environment variables configured for the spotipy client. Additionally, certain playlist names are hardcoded into the scripts, so users without the same playlist names will need to create those playlists first (i.e. bot_test and everything)


