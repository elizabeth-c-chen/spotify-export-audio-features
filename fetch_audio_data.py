import sys
import os
import tekore as tk
import pandas as pd
import math

conf = tk.config_from_file('credentials.ini')
token = tk.prompt_for_user_token(*conf, scope=tk.scope.read)
spotify = tk.Spotify(token, chunked_on=True)

# This is the primary function to be called. 
def easyrun(username,limit):
    playlistids = get_all_playlist_ids(username,limit) # Get all playlist IDs
    directorystring = 'CSV_Data_for_' + username # Name of folder to create
    os.mkdir(directorystring) # Create the folder on OS
    for playlistid in playlistids:
        # This first part sets up the dictionary needed for storing the data subsets.
        # We have to store the data as subsets to account for playlists longer than 
        # 100 tracks. Spotify's API limits the number of tracks you can retrieve in 
        # an API call to just 100 tracks. 
        numitems = get_playlist_length(playlistid)
        numsubsets = get_num_subsets(numitems)
        datasubsets = {}
        # Store each subset of tracks in the dictionary
        for index in range(numsubsets):
            datasubsets[index] = get_subset_data(playlistid,index)
        # Now we are just combining all the tracks (ID only) back into one list
        track_ids_list = []
        for key in datasubsets.keys():
            datasubset = datasubsets[key]
            for index, item in enumerate(datasubset):
                track_id = datasubset[index].track.id
                track_ids_list.append(track_id)
        # tekore's Spotify library for Python has a great feature chunked() which 
        # groups together a bunch of API calls and prevents us from getting a
        # TooManyRequests error.
        with spotify.chunked():
            # Get the audio features for the entire list of tracks on current playlist
            all_track_features_modellist = spotify.tracks_audio_features(track_ids_list)
            all_track_features = all_track_features_modellist[0:len(all_track_features_modellist)]
        df_playlist = []
        # For each track, append the data to an array.
        for item in all_track_features:
            audio_feat_as_series = pd.read_json(item.json(),typ='series')
            df_playlist.append(audio_feat_as_series)
        # Finally, set up data to export to CSV ()
        playlistname = get_playlist_name(playlistid)
        filename = playlistname.replace(" ", "")
        df_all = pd.DataFrame(df_playlist)
        # The column indices below specify the audio features I wanted to analyze
        df_filtered = df_all.iloc[:, [1,3,5,6,7,8,9,11,12,17]].copy()
        df_filtered.to_csv(directorystring + '/' + filename + '_data.csv')

# Helper function to retrieve playlist IDs for a user.
def get_all_playlist_ids(username,limit):
    listplaylists = spotify.playlists(username, limit=limit)
    playlistids = []
    for item in listplaylists.items:
        playlistids.append(item.id)
    return playlistids

# Helper function to determine how many data subsets we will need.
def get_num_subsets(x):
    return int(math.ceil(x / 100.0))

# Helper function to get the length of a playlist (for subsetting).
def get_playlist_length(playlistid):
    playlistitems = spotify.playlist_items(playlistid, fields=['total'])
    return playlistitems['total']

# Helper function to get playlist name for writing data to file.
def get_playlist_name(playlistid):
    playlist = spotify.playlist(playlistid, fields=['name'])
    return playlist['name']

# Helper function to get items from a playlist with specified offsetcount.
def get_subset_data(playlistid,offsetcount):
    offset = offsetcount*100
    return spotify.playlist_items(playlistid, limit=100, offset=offset).items


try:
    username = sys.argv[1]
    num_playlists = sys.argv[2]
    easyrun(username, num_playlists)
except: 
    print("""
        Usage: python3 fetch_audio_data.py spotify_username integer_num_of_playlists_to_retrieve
        """)
