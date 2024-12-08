# Yoinkify - Spotify Playlist Forker
<p align="left">
  <img src="static\yoinkfav.png" width="75" >
</p>

## Project Structure
```
yoinkify/
│
├── static/
│   └── spotify.png
│   └── yoinkifav.png 
│   └── css/
│       └── tailwind.css
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── preview.html
│   └── success.html
│
├── app.py
├── spotify_utils.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies
```bash
pip install flask spotipy python-dotenv
pip install tailwindcss
```

3. Spotify Developer Configuration
- Go to https://developer.spotify.com/dashboard/
- Create a new application
- Set Redirect URI to `http://localhost:5000/callback`
- Create a `.env` file with:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
SECRET_KEY=your_flask_secret_key
```

4. Run the application
```bash
python app.py
```

## Notes
- Ensure you have Python 3.8+ installed
- Keep your Spotify credentials confidential
- This app requires user interaction with Spotify's OAuth flow
