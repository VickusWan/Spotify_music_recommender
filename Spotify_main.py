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
                   
    def clean_lists(self):
        self.ids.clear()
        self.artists.clear()
        self.explicit.clear()
        self.name.clear()
        self.pop.clear()
        self.rel_date.clear()
        
    def remove_char(self, word):
        word=word.replace('[','').replace(']','').replace("'",'').replace(',','').lower()
        return word
    
    def select_artist(self, song, artist):
        song = song.lower()
        artist = artist.lower()
        search = self.get_track_id(song)
        
        selection_id = "does not exist"
        
        for i in range(search.shape[0]):
            name = self.remove_char(str(search['Artists'][i]))
            if artist in name:
                selection_id = search.iloc[i,2]
                break
        
        return selection_id
      
        
    def track_input_model(self, ids):
        track_detail = self.track(ids)
        print(track_detail.columns)
        track_detail['year']=track_detail['year'].astype(float)
        track_detail.drop(['artists', 'id', 'name', 'release_date'], axis=1, inplace=True)
        return track_detail
        
        
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
        
    
    def get_artist_id(self, artist_name):
        dummy = []
        search = self.spotify.search(q=artist_name, type='artist')
        
        for i in search['artists']['items']:
            dummy.append([i['id'], i['name'], i['genres']])
        
        artist_id = pd.DataFrame(dummy)
        artist_id.columns = ['id', 'Artist Name', 'Genres']
        return artist_id
    
    def get_track_id(self, track_name):
        dummy = []
        search = self.spotify.search(q=track_name, type='track')
        for i in search['tracks']['items']:
            dummy.append([i['name'], [j['name'] for j in i['artists']], i['id']])
        
        track_id = pd.DataFrame(dummy)
        track_id.columns = ['Song name', 'Artists', 'id']
        return track_id
          
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
    
    def playlist(self, playlist_id):

        pl=self.spotify.playlist_tracks(playlist_id=playlist_id)
        
        for i in pl['items']:
            self.artists.append([x['name'] for x in i['track']['artists']])
            if i['track']['explicit'] == False:
                self.explicit.append(0)
            else:
                self.explicit.append(1)
            self.name.append(i['track']['name'])
            self.pop.append(i['track']['popularity'])
            self.rel_date.append(i['track']['album']['release_date'])
            self.ids.append(i['track']['id'])
            
        year = [d[:4] for d in self.rel_date]
        
        audio_features = self.get_audio_features(self.ids)
            
        rest = pd.DataFrame(list(zip(self.explicit, self.artists, self.name, self.rel_date, year, self.pop)))
        self.clean_lists()
        return self.get_full_data(rest, audio_features)
    
    def related_artists(self, artist_name):
        related_artists = []
        artist_id = self.get_artist_id(artist_name).iloc[0,0]
        search = self.spotify.artist_related_artists(artist_id)
        for i in search['artists']:
            related_artists.append([i['name'], i['id']])
        
        return pd.DataFrame(related_artists)
        
        
        
        