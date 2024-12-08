import re

def extract_playlist_id(playlist_url):
    """Extract playlist ID from Spotify URL"""
    match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
    if not match:
        raise ValueError("Invalid Spotify playlist URL")
    return match.group(1)

def get_playlist_details(sp, playlist_url):
    """
    Fetch detailed information about a Spotify playlist
    
    Args:
        sp (spotipy.Spotify): Authenticated Spotify client
        playlist_url (str): URL of the Spotify playlist
    
    Returns:
        dict: Playlist details including name, description, tracks, etc.
    """
    playlist_id = extract_playlist_id(playlist_url)
    
    # Fetch playlist details
    playlist = sp.playlist(playlist_id)
    
    # Fetch all tracks (pagination)
    tracks_response = sp.playlist_tracks(playlist_id)
    tracks = tracks_response['items']
    
    while tracks_response['next']:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response['items'])
    
    # Process track details
    processed_tracks = []
    for item in tracks:
        track = item['track']
        processed_tracks.append({
            'name': track['name'],
            'artists': ', '.join([artist['name'] for artist in track['artists']]),
            'duration_ms': track['duration_ms'],
            'uri': track['uri']
        })
    
    return {
        'id': playlist_id,
        'name': playlist['name'],
        'description': playlist.get('description', ''),
        'owner': playlist['owner']['display_name'],
        'images': playlist['images'],
        'tracks': processed_tracks
    }

def fork_playlist(sp, playlist_details):
    """
    Create a new playlist in user's account with the same tracks
    
    Args:
        sp (spotipy.Spotify): Authenticated Spotify client
        playlist_details (dict): Details of the original playlist
    
    Returns:
        dict: New playlist details
    """
    # Get current user
    user_id = sp.me()['id']
    
    # Create descriptive forked playlist description
    forked_description = (
        f"Forked from {playlist_details['owner']}'s playlist: {playlist_details['name']}. "
        "Original playlist description: " + 
        (playlist_details['description'][:200] + '...' if len(playlist_details['description']) > 200 else playlist_details['description'])
    )
    
    # Create new playlist
    new_playlist = sp.user_playlist_create(
        user=user_id, 
        name=f"Forked: {playlist_details['name']}", 
        public=False,
        description=forked_description
    )
    
    # Add tracks to new playlist
    track_uris = [track['uri'] for track in playlist_details['tracks']]
    
    # Spotify API has a limit of 100 tracks per request
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(new_playlist['id'], track_uris[i:i+100])
    
    return new_playlist