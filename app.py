'''
Name: Sreehari Sreekumar Nair
Date: Febraury 9, 2025
Purpose: Program to recommend music based on the user's input.
'''

import streamlit as st
import pickle
import pandas as pd
import requests
import base64

def get_spotify_token(client_id, client_secret):
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response_data = response.json()
    
    return response_data['access_token']

def fetch_poster(music_title):
    client_id = "9d86721b737840098d4276c9ee060d3b"
    client_secret = "b98a17a4fe1b4871af3cec0d0ad8ca25"
    access_token = get_spotify_token(client_id, client_secret)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    search_url = f"https://api.spotify.com/v1/search?q={music_title}&type=track&limit=1"
    response = requests.get(search_url, headers=headers)
    data = response.json()
    
    if 'tracks' in data and data['tracks']['items']:
        album_image_url = data['tracks']['items'][0]['album']['images'][0]['url']
        return album_image_url
    else:
        return None  

def recommend(musics):
    music_index = music[music['track_name'] == musics].index[0]
    
    song_genre = music.iloc[music_index]['playlist_genre']
    
    genre_music = music[music['playlist_genre'] == song_genre]
    
    recommended_music = []
    recommended_music_poster = []
    
    distances = similarity[music_index]  
    music_list = []
    
    for i in genre_music.index:
        if i != music_index:  
            music_list.append((i, distances[i]))  
    
    
    music_list = sorted(music_list, key=lambda x: x[1], reverse=True)
    
    
    for i in range(min(5, len(music_list))):
        music_id = music.iloc[music_list[i][0]].track_name
        if music_id not in recommended_music:
            recommended_music.append(music_id)
            recommended_music_poster.append(fetch_poster(music_id))
    
    return recommended_music, recommended_music_poster


music_dict = pickle.load(open(r'C:\\Users\\sreeh\\musicrec.pkl', 'rb'))
music = pd.DataFrame(music_dict)

similarity = pickle.load(open(r'C:\\Users\\sreeh\\similarities.pkl', 'rb'))

st.title('Music Recommender System')

selected_music_name = st.selectbox('Select a music you like', music['track_name'].values)

recommended_music, recommended_music_poster = recommend(selected_music_name)

if st.button('Recommend'):
    names, posters = recommend(selected_music_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])