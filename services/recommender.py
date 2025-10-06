import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

MOOD_PARAMS = {
    "happy/energetic": {
        "target_valence": 0.8,
        "target_energy": 0.7,
        "seed_genres": ["pop", "dance", "edm"]
    },
    "chill/reflective": {
        "target_valence": 0.5,
        "target_energy": 0.3,
        "seed_genres": ["chill", "acoustic", "indie"]
    },
    "sad/melancholic": {
        "target_valence": 0.2,
        "target_energy": 0.3,
        "seed_genres": ["sad", "alt-rock", "singer-songwriter"]
    }
}


def get_spotify_client():
    cid = os.getenv("SPOTIFY_CLIENT_ID")
    secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not cid or not secret:
        raise RuntimeError("Spotify credentials missing.")
    return Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))


def recommend_tracks(mood: str, limit: int = 10):
    params = MOOD_PARAMS.get(mood)
    if not params:
        return []
    try:
        sp = get_spotify_client()
        recs = sp.recommendations(
            seed_genres=params["seed_genres"],
            target_valence=params["target_valence"],
            target_energy=params["target_energy"],
            limit=limit
        )
        tracks = []
        for t in recs["tracks"]:
            name = t["name"]
            artists = ", ".join([a["name"] for a in t["artists"]])
            url = t["external_urls"]["spotify"]
            tracks.append({"name": name, "artist": artists, "url": url})
        return tracks
    except Exception:
        return []
