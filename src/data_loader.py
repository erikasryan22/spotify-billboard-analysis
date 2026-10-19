from pathlib import Path
import zipfile

import gdown
import pandas as pd


DATASETS = {
    "SpotifyFeatures.csv": "1KvG1T9rL6gOqmOO-VDOpO4PhKUdFU2Lh",
    "hot-100-current.csv": "1iqefQOCEMdTs4lKZTguRexnGYi0TWCHO",
}


def load_data(data_dir):
    """Reuse local CSVs or archives; download the existing mirrors when missing."""
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    for filename, file_id in DATASETS.items():
        target = data_dir / filename
        if target.is_file():
            continue
        archive_path = data_dir / f"{target.stem}.zip"
        try:
            if not zipfile.is_zipfile(archive_path):
                gdown.download(id=file_id, output=str(archive_path), quiet=False)
            with zipfile.ZipFile(archive_path) as archive:
                members = {Path(name).name: name for name in archive.namelist()}
                target.write_bytes(archive.read(members[filename]))
        except (OSError, KeyError, zipfile.BadZipFile, gdown.exceptions.FileURLRetrievalError) as error:
            raise FileNotFoundError(
                f"Could not prepare {filename}. Download it using the README source links, "
                f"place it in {data_dir.resolve()}, then run this cell again."
            ) from error
    return pd.read_csv(data_dir / "SpotifyFeatures.csv"), pd.read_csv(data_dir / "hot-100-current.csv")
