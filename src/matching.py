import re


def normalize_text(value):
    """Normalize typography while retaining accents, collaborators and version words."""
    value = str(value).casefold().replace("&", " and ").replace("+", " and ")
    value = re.sub(r"\b(?:featuring|feat|ft)\.?\s+", " feat ", value)
    value = re.sub(r"[^\w\s]", " ", value).replace("_", " ")
    return re.sub(r"\s+", " ", value).strip()


def match_songs(hot100, spotify_tracks):
    """Match full normalized credits only when they identify one Spotify track."""
    keys = ["song_clean", "artist_clean"]
    spotify = spotify_tracks.loc[spotify_tracks["identity_consistent"]].copy()
    spotify["song_clean"] = spotify["track_name"].map(normalize_text)
    spotify["artist_clean"] = spotify["artist_name"].map(normalize_text)
    spotify = spotify.loc[spotify[keys].ne("").all(axis=1)]
    spotify = spotify.loc[~spotify.duplicated(keys, keep=False)]
    chart = hot100.copy()
    chart["song_clean"] = chart["title"].map(normalize_text)
    chart["artist_clean"] = chart["performer"].map(normalize_text)
    chart = chart.loc[chart[keys].ne("").all(axis=1)]
    chart = chart.sort_values("current_week").drop_duplicates(["chart_week"] + keys)
    merged = chart.merge(spotify, on=keys, how="left", validate="many_to_one")
    matched = merged.loc[merged["track_id"].notna()].copy()
    if matched.empty:
        raise ValueError("No unambiguous songs matched. Check the input datasets and song/artist credits.")
    return merged, matched
