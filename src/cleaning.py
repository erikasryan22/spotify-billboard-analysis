import numpy as np
import pandas as pd


def clean_spotify(raw):
    """Validate features, average track popularity, and retain genre membership."""
    spotify = raw.dropna(subset=["track_id", "track_name", "artist_name"]).copy()
    spotify["genre"] = spotify["genre"].fillna("Unknown").str.replace("’", "'", regex=False)
    numeric = ["popularity", "acousticness", "danceability", "duration_ms", "energy",
               "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence"]
    spotify[numeric] = spotify[numeric].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
    for feature in ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "speechiness", "valence"]:
        spotify[feature] = spotify[feature].where(spotify[feature].between(0, 1))
    spotify["popularity"] = spotify["popularity"].where(spotify["popularity"].between(0, 100))
    spotify["tempo"] = spotify["tempo"].where(spotify["tempo"] > 0)
    spotify["popularity"] = spotify.groupby("track_id")["popularity"].transform("mean")
    name_counts = spotify.groupby("track_id")[["track_name", "artist_name"]].nunique()
    consistent_ids = name_counts.index[name_counts.max(axis=1).eq(1)]
    spotify = spotify.drop_duplicates(["track_id", "genre"])
    tracks = spotify.drop_duplicates("track_id").copy()
    tracks["identity_consistent"] = tracks["track_id"].isin(consistent_ids)
    tracks["genres"] = tracks["track_id"].map(spotify.groupby("track_id")["genre"].agg(list))
    return spotify, tracks


def clean_hot100(raw):
    """Remove invalid chart rows and conflicting positions, then add chart decades."""
    hot100 = raw.dropna(subset=["title", "performer"]).copy()
    hot100["chart_week"] = pd.to_datetime(hot100["chart_week"], errors="coerce")
    hot100["current_week"] = pd.to_numeric(hot100["current_week"], errors="coerce")
    valid = hot100["chart_week"].notna() & hot100["current_week"].between(1, 100) & hot100["current_week"].mod(1).eq(0)
    hot100 = hot100.loc[valid].drop_duplicates(["chart_week", "current_week", "title", "performer"])
    conflicts = hot100.duplicated(["chart_week", "current_week"], keep=False)
    print("Rows excluded for conflicting chart positions:", int(conflicts.sum()))
    hot100 = hot100.loc[~conflicts].copy()
    hot100["year"] = hot100["chart_week"].dt.year
    hot100["decade"] = (hot100["year"] // 10) * 10
    return hot100
