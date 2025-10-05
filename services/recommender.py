import osimport os

from spotipy import Spotifyfrom spotipy import Spotify

from spotipy.oauth2 import SpotifyClientCredentialsfrom spotipy.oauth2 import SpotifyClientCredentials



MOOD_PARAMS = {MOOD_PARAMS = {

    "happy/energetic": {    "happy/energetic": {

        "target_valence": 0.8,        "target_valence": 0.8,

        "target_energy": 0.7,        "target_energy": 0.7,

        "seed_genres": ["pop", "dance", "edm"]        "seed_genres": ["pop", "dance", "edm"]

    },    },

    "chill/reflective": {    "chill/reflective": {

        "target_valence": 0.5,        "target_valence": 0.5,

        "target_energy": 0.3,        "target_energy": 0.3,

        "seed_genres": ["chill", "acoustic", "indie"]        "seed_genres": ["chill", "acoustic", "indie"]

    },    },

    "sad/melancholic": {    "sad/melancholic": {

        "target_valence": 0.2,        "target_valence": 0.2,

        "target_energy": 0.3,        "target_energy": 0.3,

        "seed_genres": ["sad", "alt-rock", "singer-songwriter"]        "seed_genres": ["sad", "alt-rock", "singer-songwriter"]

    }    }

}}



def get_spotify_client():

    cid = os.getenv("SPOTIFY_CLIENT_ID")def get_spotify_client():

    secret = os.getenv("SPOTIFY_CLIENT_SECRET")    cid = os.getenv("SPOTIFY_CLIENT_ID")

    if not cid or not secret:    secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        raise RuntimeError("Spotify credentials missing.")    if not cid or not secret:

    return Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))        raise RuntimeError("Spotify credentials missing.")

    return Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))

def recommend_tracks(mood: str, limit: int = 10):

    params = MOOD_PARAMS.get(mood)

    if not params:def recommend_tracks(mood: str, limit: int = 10):

        return []    params = MOOD_PARAMS.get(mood)

    try:    if not params:

        sp = get_spotify_client()        return []

        recs = sp.recommendations(    try:

            seed_genres=params["seed_genres"],        sp = get_spotify_client()

            target_valence=params["target_valence"],        recs = sp.recommendations(

            target_energy=params["target_energy"],            seed_genres=params["seed_genres"],

            limit=limit            target_valence=params["target_valence"],

        )            target_energy=params["target_energy"],

        tracks = []            limit=limit

        for t in recs["tracks"]:        )

            name = t["name"]        tracks = []

            artists = ", ".join([a["name"] for a in t["artists"]])        for t in recs["tracks"]:

            url = t["external_urls"]["spotify"]            name = t["name"]

            tracks.append({"name": name, "artist": artists, "url": url})            artists = ", ".join([a["name"] for a in t["artists"]])

        return tracks            url = t["external_urls"]["spotify"]

    except Exception:            tracks.append({"name": name, "artist": artists, "url": url})

        return []        return tracks

    except Exception:
        return []
