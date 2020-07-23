# Python Script for use with Spotify API

This is a (still work-in-progress) tool to get your audio features data for each track on a playlist from the Spotify API. The output after running the script is a new directory containing CSV files of audio features (one row per track, one file per playlist) for the first `num_playlists` playlists you specified in the arguments (chosen from however you have ordered your playlists).

You need a Developer account to use it as is (you can get one at https://developer.spotify.com/dashboard/). Once you've created an app, you can copy and paste your client ID, client secret, and the redirect URI into the config.py file. You have to specify the redirect URI in Edit Settings when you click on your app from the Dashboard. The redirect URI can just be http://localhost/. NOTE: the page won't load anything, but you just need to copy the url you were redirected to from your browser into the command line below where it says "Please paste redirect URL:". The script should run after you paste the redirect URL.

Usage:  
```python3 config.py```   
```python3 fetch_audio_data.py spotify_username num_playlists```

Arguments:
* `spotify_username` (str): your spotify username (if you don't know it, you can find out by logging in to https://www.spotify.com/ and visiting your Account Overview)
* `num_playlists` (int): desired number of playlists to get data for 

Future Goals:
* Implement data analysis with stats and plots
* Use ML to judge how likely you are to enjoy a specific song
* Compare your data with a friend's data and see compatibility
