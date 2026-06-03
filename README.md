# earthcare_aerosol_cloud_interactions

Analysis of aerosol–cloud interactions through K-means clustering of EarthCARE
single-instrument and synergy products. Project for **ESA Science Hub Challenge #1**
— ESRIN Frascati (RM), Italy — September 2025.

The analysis lives entirely in Jupyter notebooks and is designed to run on the
**MAAP JupyterHub / PAL** (NASA–ESA Multi-Mission Algorithm and Analysis
Platform), where the EarthCARE Level-2 products are reachable via PYSTAC. Data
access needs a **MAAP bearer token** (10-hour validity) saved as `token.txt` in
the project root.

## Regions of interest

| Region | Box | Orbit frame | Filename suffix |
|--------|-----|-------------|-----------------|
| West Pacific | 100–160°E, 0–20°N | A / E | *(none)* |
| East Pacific | 160–100°W, 0–20°N | A / E | `_EP` |
| Antarctica (Ross Sea) | 80–60°S, 160°E–140°W | G | `_AN` |

The Ross Sea straddles the antimeridian, so the AN notebooks search the polar
**frame `G`** and filter spatially in the **0–360° convention** (160–220°)
instead of using a bbox.

## Pipeline at a glance

```
EDA notebooks (PYSTAC, need token.txt)            merger                  analysis
  ac__tc__2b[_EP/_AN].ipynb  → AC__TC__2B_1s{,_EP,_AN}.nc  ┐
  cpr_cld_2a[_EP/_AN].ipynb  → CPR_CLD_2A_1s{,_EP,_AN}.nc  ├→ merger[,_EP,_AN] → challenge_1min_*{,_EP,_AN}.nc → kmeans[,_EP,_AN] / report
  atl_ald_2a.ipynb / _AN     → aot_resampled_{wp,ep,an}.nc ┘
```

1. **EDA / extract** — each EDA notebook queries the MAAP catalog for one
   product over one region, resamples to 1 s, and saves a raw `*_1s*.nc`
   (AOT files are named `aot_resampled_<region>.nc`).
2. **Merge** (`merger*.ipynb`) — outer-join the three products on time, fill
   clear-sky NaNs with 0, resample to 1-minute pixels (numerical → mean,
   `stc_*` labels → mode), and save `challenge_1min_numerical*.nc` and
   `challenge_1min_complete*.nc`.
3. **Cluster** (`kmeans*.ipynb`) — filter to the region box (ocean only,
   `land_flag < 0.1`), `log1p`-normalise AOT/IWP/LWP, choose *k* via the elbow
   method, fit K-means, and cross-reference clusters with the `stc_*` synergetic
   classification.
4. **Report** (`report.ipynb`) — self-contained three-region comparison; re-runs
   preprocessing + clustering via `prepare_region()` and produces the figures.

## Notebook map

| Notebook | Region | Produces |
|----------|--------|----------|
| `ac__tc__2b.ipynb` / `_EP` / `_AN` | WP / EP / AN | `AC__TC__2B_1s{,_EP,_AN}.nc` |
| `cpr_cld_2a.ipynb` / `_EP` / `_AN` | WP / EP / AN | `CPR_CLD_2A_1s{,_EP,_AN}.nc` |
| `atl_ald_2a.ipynb` | WP + EP | `aot_resampled_{wp,ep}.nc` |
| `atl_ald_2a_AN.ipynb` | AN | `aot_resampled_an.nc` |
| `merger.ipynb` / `_EP` / `_AN` | WP / EP / AN | `challenge_1min_*{,_EP,_AN}.nc` |
| `kmeans.ipynb` / `_EP` / `_AN` | WP / EP / AN | clustering + figures |
| `report.ipynb` | all three | comparison figures (`*.png`) |
| `OpenChallangeNotebook-Ch1-*.ipynb` | — | original submission, full narrative |
| `atl_tc_2a_Antarctica_SLC.ipynb` | AN | ATLID quicklook only (not in pipeline) |
| `cpr_fmr_2a_ITA_radarDPC.ipynb` | Italy | radar comparison with DPC |

## Getting started on the MAAP PAL

> The `*.nc` data files are **git-ignored** and are *not* in the repository —
> they must be regenerated on the PAL.

1. Create the conda environment (see `Setup_guide.md`) and register the
   `earthcare` kernel.
2. Clone this repo on the PAL and put your MAAP bearer token in `token.txt`.
3. Check what still needs producing:
   ```bash
   python check_data.py
   ```
4. Regenerate the missing data **in order** (EDA → merger), per region:
   - `ac__tc__2b{,_EP,_AN}.ipynb`, `cpr_cld_2a{,_EP,_AN}.ipynb`,
     `atl_ald_2a.ipynb` + `atl_ald_2a_AN.ipynb`
   - then `merger{,_EP,_AN}.ipynb`
5. Re-run `check_data.py` — when everything is present, run `kmeans*.ipynb`
   and `report.ipynb`.

## Open methodology questions (before finalising `report.ipynb`)

- **Elbow check:** confirm `k=5` is still the right choice on all three regions
  *after* the `log1p` transform — re-run the elbow plots before fixing *k*.
- **AN orbit frame:** the AN notebooks assume polar **frame `G`**; verify on the
  catalog that frame `G` is the one covering the Ross Sea band and adjust if the
  matched-item count looks wrong.
- **stc cross-reference:** present as **percentage composition** per cluster so
  the three regions stay comparable despite different dataset sizes.

See `update_report.ipynb` for the full methodology change log.
