# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 20:08:45 2021

@author: Victor
"""

import pandas as pd
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

def recommend_song(track_detail):
    distances, indices = model_knn.kneighbors(track_detail.values.reshape(1, -1), n_neighbors = 2)
    return music.iloc[indices.flatten()[1],:]['name'], music.iloc[indices.flatten()[1],:]['artists']

music = pd.read_csv('data.csv')

# =============================================================================
# outfile = open('data', 'wb')
# pickle.dump(music, outfile)
# outfile.close()
# =============================================================================

music['name']=music['name'].str.lower()
year = music['year']
name = music['name']
song_id = music['id']
music_feat = music.drop(['artists', 'id', 'release_date', 'name'], axis=1)

col = music_feat.columns.to_list()
min_max_scaler = MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(music_feat)
norm = pd.DataFrame(x_scaled)
norm.columns = col
norm.set_index(song_id, inplace=True)

model_knn = NearestNeighbors(n_neighbors=10, metric='minkowski', p=1)
model_knn.fit(norm)

# =============================================================================
# outfile2 = open('data_normalized', 'wb')
# pickle.dump(norm, outfile2)
# outfile2.close()
# 
# knn_data = open('knn_model', 'wb')
# pickle.dump(model_knn, knn_data)
# knn_data.close()
# =============================================================================

