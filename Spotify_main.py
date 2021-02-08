# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 15:43:03 2021

@author: Victor
"""

import Spotify_Authorization
import spotipy
import pandas as pd

class Spotify_app():
    def __init__(self):
            self.auth = Spotify_Authorization.auth()
            self.spotify = spotipy.Spotify(auth_manager=self.auth)
            self.ids = []
            self.artists = []
            self.explicit = []
            self.name = []
            self.pop = []
            self.rel_date = []
            

    def playlist(self, playlist_id):

        pl=self.spotify.playlist_tracks(playlist_id=playlist_id)
        
        for i in range(len(pl['items'])):
            self.artists.append([x['name'] for x in pl['items'][i]['track']['artists']])
            if pl['items'][i]['track']['explicit'] == False:
                self.explicit.append(0)
            else:
                self.explicit.append(1)
            self.name.append(pl['items'][i]['track']['name'])
            self.pop.append(pl['items'][i]['track']['popularity'])
            self.rel_date.append(pl['items'][i]['track']['album']['release_date'])
            self.ids.append(pl['items'][i]['track']['id'])
            
        year = [d[:4] for d in self.rel_date]
        
        audio_features = self.get_audio_features(self.ids)
            
        rest = pd.DataFrame(list(zip(self.explicit, self.artists, self.name, self.rel_date, year, self.pop)))
        self.clean_lists()
        return self.get_full_data(rest, audio_features)
        
    
    def artist_toptracks(self, artist_id):
        
        artist = self.spotify.artist_top_tracks(artist_id)
        
        for i in artist['tracks']:
            self.artists.append(([x['name'] for x in i['artists']]))
            if i['explicit'] == False:
                self.explicit.append(0)
            else:
                self.explicit.append(1)
            self.name.append(i['name'])
            self.pop.append(i['popularity'])
            self.ids.append(i['id']) 
            self.rel_date.append(self.spotify.track(i['id'])['album']['release_date'])
        year = [d[:4] for d in self.rel_date]
        
        audio_features = self.get_audio_features(self.ids)
        
        rest = pd.DataFrame(list(zip(self.explicit, self.artists, self.name, self.rel_date, year, self.pop)))
        self.clean_lists()
        
        return self.get_full_data(rest, audio_features)
        
    
    def album(self, album_id):
        album = self.spotify.album_tracks(album_id)
        for i in album['items']:
            self.artists.append([x['name'] for x in i['artists']])
            if (i['explicit']) == False:
                self.explicit.append(0)
            else:
                self.explicit.append(1)
            self.name.append(i['name'])
            self.pop.append(self.spotify.track(i['id'])['popularity'])
            self.rel_date.append(self.spotify.track(i['id'])['album']['release_date'])
            self.ids.append(i['id'])
        year = [d[:4] for d in self.rel_date]
        
        audio_features = self.get_audio_features(self.ids)
        
        rest = pd.DataFrame(list(zip(self.explicit, self.artists, self.name, self.rel_date, year, self.pop)))
        self.clean_lists()
        
        return self.get_full_data(rest, audio_features)
    
    def track(self, track_id):
        
        track = self.spotify.track(track_id)
        self.artists.append([i['name'] for i in track['artists']])
        if track['explicit'] == False:
            self.explicit.append(0)
        else:
            self.explicit.append(1)
              
        self.name.append(track['name'])
        self.pop.append(track['popularity'])
        self.ids.append(track['id']) 
        self.rel_date.append(track['album']['release_date'])
        year = [d[:4] for d in self.rel_date]
        audio_features = self.get_audio_features(self.ids)
        
        rest = pd.DataFrame(list(zip(self.explicit, self.artists, self.name, self.rel_date, year, self.pop)))
        self.clean_lists()
        
        return self.get_full_data(rest, audio_features)
        
    
    def clean_lists(self):
        self.ids.clear()
        self.artists.clear()
        self.explicit.clear()
        self.name.clear()
        self.pop.clear()
        self.rel_date.clear()
    
    def get_audio_features(self, ids):
        
        val = []
        
        for music_id in ids:
            audio = self.spotify.audio_features(music_id)
            [audio[0].pop(k) for k in ['type', 'uri', 'track_href', 'analysis_url', 'time_signature']]
            val.append([i for i in audio[0].values()])
            
        index = [i for i in audio[0].keys()]
        audio_features = pd.DataFrame(val)
        audio_features.columns = index            
        
        return audio_features
    
    def get_full_data(self, remain, audio_features):
        
        remain.columns = ['explicit', 'artists', 'name', 'release_date', 'year', 'popularity']
        data = pd.concat([audio_features, remain], axis=1)
        cols = ['acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 'explicit', 'id', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'name', 'popularity', 'release_date', 'speechiness', 'tempo', 'valence', 'year']
        data = data[cols]
        return data