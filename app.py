from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import pickle

# Loading models
df = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommendation(song):
    idx = df[df['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=False, key=lambda x: x[1])
    songs = []

    for i in distances[1:21]:
        song_name = df.iloc[i[0]].song
        youtube_link = f"https://www.youtube.com/results?search_query={'+'.join(song_name.split())}"
        spotify_link = f"https://open.spotify.com/search/{'%20'.join(song_name.split())}"
        songs.append({'name': song_name, 'youtube_link': youtube_link, 'spotify_link': spotify_link})

    return songs


app = Flask(__name__)


@app.route('/')
def index():
    names = list(df['song'].values)
    return render_template('index.html', name=names)


@app.route('/recom', methods=['POST'])
def mysong():
    user_song = request.form['names']
    songs = recommendation(user_song)
    return jsonify({'songs': songs})


if __name__ == "__main__":
    app.run(debug=True)
