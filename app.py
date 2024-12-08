import os
import spotipy
from flask import Flask, render_template, request, redirect, url_for, session
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from spotify_utils import get_playlist_details, fork_playlist

# Load environment variables
load_dotenv()

# Flask and Spotify configuration
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Spotify OAuth Scope Configuration
SPOTIPY_SCOPE = 'playlist-modify-public playlist-modify-private user-library-read'

def get_spotify_oauth():
    """Create Spotify OAuth object"""
    return SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
        scope=SPOTIPY_SCOPE
    )

@app.route('/')
def home():
    """Home page with login option"""
    return render_template('home.html')

@app.route('/login')
def login():
    """Initiate Spotify OAuth login"""
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """Handle Spotify OAuth callback"""
    sp_oauth = get_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    # Store token in session
    session['token_info'] = token_info
    return redirect(url_for('preview_playlist'))

@app.route('/preview', methods=['GET', 'POST'])
def preview_playlist():
    """Preview playlist before forking"""
    # Check if user is authenticated
    if 'token_info' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        playlist_url = request.form.get('playlist_url')
        
        # Validate Spotify playlist URL
        if not playlist_url or 'open.spotify.com/playlist/' not in playlist_url:
            return render_template('home.html', error='Invalid Spotify playlist URL')
        
        # Get Spotify client
        sp_oauth = get_spotify_oauth()
        token_info = session['token_info']
        
        # Refresh token if expired
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        try:
            # Get playlist details
            playlist_details = get_playlist_details(sp, playlist_url)
            session['playlist_details'] = playlist_details
            return render_template('preview.html', playlist=playlist_details)
        
        except Exception as e:
            return render_template('home.html', error=str(e))
    
    return render_template('home.html')

@app.route('/fork', methods=['POST'])
def fork():
    """Fork the playlist to user's account"""
    if 'token_info' not in session or 'playlist_details' not in session:
        return redirect(url_for('home'))
    
    sp_oauth = get_spotify_oauth()
    token_info = session['token_info']
    
    # Refresh token if expired
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist_details = session['playlist_details']
    
    try:
        # Fork playlist
        new_playlist = fork_playlist(sp, playlist_details)
        return render_template('success.html', 
                               playlist_name=new_playlist['name'], 
                               playlist_url=new_playlist['external_urls']['spotify'])
    
    except Exception as e:
        return render_template('home.html', error=str(e))

@app.route('/logout')
def logout():
    """Clear session and log out"""
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)