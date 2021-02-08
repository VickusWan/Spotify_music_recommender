# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 12:30:10 2021

@author: Victor
"""

import requests
import base64
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def auth():
    return auth_manager

Client_ID = 'c6d7404e014a4395b773c3b3f4c50d95'
Client_Secret = '8004465dd19444eab523311469c7a065' 

spotify_url = 'https://accounts.spotify.com/api/token'

client_creds = f"{Client_ID}:{Client_Secret}"
creds_b64 = base64.b64encode(client_creds.encode())

body = {'grant_type': 'client_credentials'}
header = {'Authorization': f"Basic {creds_b64.decode()}"}

r = requests.post(spotify_url, data = body, headers=header)

auth_manager = SpotifyClientCredentials(client_id=Client_ID, client_secret=Client_Secret)
sp = spotipy.Spotify(auth_manager=auth_manager)