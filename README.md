# Spotify Audio Features × Billboard Hot 100

An exploratory data analysis of Spotify audio features and Billboard Hot 100 chart appearances. The project examines the songs that can be matched across the two sources, with coverage checks and one-recording analysis units.

## Questions

1. How do audio features differ across chart decades in the matched sample?
2. Do recordings reaching the Top 10 differ from those peaking at 51–100?
3. Which genre labels are most common, and how do their average features differ?
4. Which recordings combine low valence with high snapshot popularity, or a slow tempo with a Top 10 peak?

## Key findings

<!-- RESULTS_START -->
- Matched **6,922/31,327** unique song–artist keys (**22.1%**).
- Top 10 minus 51–100 median energy: **-0.060** (descriptive difference).
- Most represented matched genre: **Country**, with **1090.0** weighted recordings.

![Decade trends](figures/decade_trends.png)

![Rank comparisons](figures/rank_comparison.png)
<!-- RESULTS_END -->

In the saved analysis, the Top 10 and 51–100 groups contain **1,980** and **2,207** recordings, respectively. A negative median-energy difference means the Top 10 median is lower. This is a descriptive comparison; no statistical-significance test was performed.

Genre labels come from the Spotify dataset. A recording with two labels contributes 0.5 to each, so the genre totals are fractional counts rather than counts of distinct recordings in mutually exclusive genres.

## Run locally with Anaconda / Jupyter

Use Python 3.10 or newer. Download or clone the complete project, then open Anaconda Prompt or a terminal in its root folder:

```bash
conda create -n spotify python=3.11 pip
conda activate spotify
python -m pip install -r requirements.txt
jupyter lab
```

Start Jupyter from the activated `spotify` environment, open [notebooks/analysis.ipynb](notebooks/analysis.ipynb), and select **Run → Run All Cells**. Save the notebook afterward to retain its tables and plots.

The notebook works when Jupyter starts in either the project root or the notebooks folder. Keep the src folder alongside notebooks; downloading the notebook alone is insufficient. No Colab account or system unzip command is needed.

For later sessions, activate the spotify environment and launch JupyterLab from the project folder.

## Project files

| Path | Purpose |
| --- | --- |
| notebooks/analysis.ipynb | Questions, exploratory analysis, static plots and calculated Key findings |
| src/data_loader.py | Local CSV reuse, Drive download, archive reading and manual-download guidance |
| src/cleaning.py | Spotify feature validation, popularity aggregation and chart-row cleaning |
| src/matching.py | Text normalization and conservative song–artist matching |
| data/ | Generated local data folder; excluded from Git |
| figures/ | Generated decade-trend and rank-comparison PNGs; include them in GitHub |
| requirements.txt | Analysis packages and JupyterLab |
| LICENSE | MIT license for the project code |

## Data sources

| Input | Original source | License reference |
| --- | --- | --- |
| SpotifyFeatures.csv | [Spotify Tracks DB — Zaheen Hamidani, Kaggle](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db) | Check the upstream dataset license. |
| hot-100-current.csv | [UT Data Billboard archive](https://github.com/utdata/rwd-billboard-data) | Repository code: [MIT](https://github.com/utdata/rwd-billboard-data/blob/main/LICENSE); check upstream terms for chart data. |

Place CSVs obtained from the original sources in data/ using the exact filenames above. They will be reused without downloading anything.

If local CSVs are absent, the loader tries these existing Drive mirrors:

- [Spotify archive](https://drive.google.com/file/d/1KvG1T9rL6gOqmOO-VDOpO4PhKUdFU2Lh/view)
- [Hot 100 archive](https://drive.google.com/file/d/1iqefQOCEMdTs4lKZTguRexnGYi0TWCHO/view)

Drive mirrors depend on public access and quota. If a download fails, download the corresponding CSV manually from an original source, place it in data/, and rerun the loading cell. Valid downloaded ZIPs are also reused. The mirrored snapshots may differ from current upstream releases.

Raw CSVs and source archives are not included in the repository.

## Analysis and results

See the notebook for coverage by chart decade, the full feature and rank-group comparisons, and the thresholds behind these descriptive findings.

## Interpretation limits

- Results describe only the matched subset. Unmatched songs can reflect recordings absent from the Spotify sample, differences in song titles or artist credits, or ambiguous identities excluded by the matching rules; these reasons were not separately quantified.
- Coverage varies by chart decade. In the saved run, only **61/3,024 (2.0%)** song–artist keys matched for the 2020s. This decade is weakly represented and should not be treated as representative of all its Hot 100 songs.
- Chart decade means chart presence, not release date. The 1950s cover only 1958–59, and boundary decades can be incomplete.
- Matching preserves full artist credits, accents and version words. Ambiguous Spotify identities are excluded, and differently credited collaborations can remain unmatched. Matching names does not verify historical recording versions.
- Popularity is averaged across available source rows per track ID before genre deduplication. It summarizes undated snapshot values, rather than historical chart success or a necessarily current single-date score. Other track-level fields retain the first row.
- Recordings contribute once per chart decade to trends and once overall to best-rank comparisons. Multi-genre recordings contribute fractional weights totaling one to matched genre summaries.
- Valence measures musical positiveness, not listener mood. Plots, median differences and threshold examples are descriptive; they do not establish causes or statistical significance.

## License

The project code is released under the [MIT License](LICENSE). Datasets remain subject to their original terms; this license does not relicense the Spotify or Billboard data.
