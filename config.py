import tekore as tk

"""
TODO Change the three fields below to your Spotify Developer Client ID, Client Secret, 
 and your specified Redirect URI (access via the green "Edit Settings" button) 

TODO Run python3 config.py to create the credentials.ini file 
"""

client_id = "Insert your Client ID here"
client_secret = "Insert your Client Secret here"
redirect_uri = "Insert URI for redirect here (example: http://localhost/)"

conf = (client_id, client_secret, redirect_uri)
tk.config_to_file('credentials.ini', conf)