# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 20:02:40 2021

@author: Victor
"""

from flask import Flask, request, render_template
import Spotify_main as sp
import knn_model as knn
import pickle

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recsong',methods=['GET' ,'POST'])
def recsong():
    
    spot = sp.Spotify_app()
    
    if request.method == 'POST':
    
        song=request.form['song_name']
        artist=request.form['artist_name']
        
        ids=spot.select_artist(song,artist)
        track_detail = spot.track_input_model(ids)
        
        name_output, artist_output = knn.recommend_song(track_detail)
        
        return render_template('Spotify.html', recommended_song='Song recommendation is {name} by {artist}'.format(name=name_output, artist=artist_output))
    
    return render_template('Spotify.html')
    


@app.route('/findsong',methods=['POST'])
def findsong():
    

    print([x for x in request.form.values()])

    return render_template('Spotify.html', song_found='Song recommendation is $ {}'.format(str([x for x in request.form.values()])))


if __name__ == "__main__":
    app.run()