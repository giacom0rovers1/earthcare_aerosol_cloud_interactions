# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research project analyzing aerosol-cloud interactions using EarthCARE satellite data with unsupervised machine learning (K-means clustering). Submitted for ESA Science Hub Challenge #1 (ESRIN Frascati, Sept 2025). All analysis lives in Jupyter notebooks — there are no Python modules or standalone scripts.

## Environment Setup

The project uses a Conda environment. From `Setup_guide.md`:

```bash
conda create -p ./conda_envs/earthcare -c conda-forge numpy scipy xarray pandas h5py h5netcdf netcdf4 cftime zarr pystac-client fsspec matplotlib tqdm aiohttp requests ipykernel seaborn scikit-learn
source activate /home/jovyan/conda_envs/earthcare
python -m ipykernel install --user --name earthcare --display-name "Python (earthcare_kernel)"
```

Designed to run on **MAAP JupyterHub** (NASA/ESA Multi-Mission Algorithm and Analysis Platform). Data access requires a bearer token for MAAP authentication (10-hour validity).

## Data Sources & Products

Three EarthCARE Level-2 products accessed via PYSTAC from the MAAP catalog:

| Product | Instrument | Key Variables |
|---------|-----------|---------------|
| `ATL_ALD_2A` | ATLID (lidar) | `aerosol_optical_thickness_355nm` (AOT) |
| `CPR_CLD_2A` | Cloud Profiling Radar | `ice_water_path` (IWP), `liquid_water_path` (LWP), `land_flag` |
| `AC__TC__2B` | Synergetic | `stc_2500` … `stc_20000` (target classification at altitude levels) |

The synergetic target classification (`stc_*`) uses integer codes: 0=ground, 1=clear sky, 5–7=precipitation, 8–11=liquid clouds, 13–21=ice clouds, 26–34=aerosol types (dust, sea salt, pollution, smoke).

## Regions of Interest

- **West Pacific:** 100–160°E, 0–20°N (anthropogenic + biomass burn aerosols)
- **East Pacific:** 160–100°W, 0–20°N (sea salt aerosols) — suffix `_EP` in filenames
- **Antarctica R1:** 160–180°E, 80–60°S
- **Antarctica R2:** 180–140°W, 80–60°S

## Analysis Pipeline

**Step 1 — Merge (`merger.ipynb` / `merger_EP.ipynb`):**
1. Load all three products for a geographic region
2. Merge on time/space with outer join, fill NaN → 0 (clear-sky assumption)
3. Resample to 1-minute intervals (numerical vars → mean; classification labels → mode)
4. Output: `challenge_1min_complete.nc`, `challenge_1min_numerical.nc`, `challenge_1min_labels.nc`

**Step 2 — Cluster (`kmeans.ipynb` / `kmeans_EP.ipynb`):**
1. Load `challenge_1min_numerical.nc`, filter to bounding box
2. Min-max normalize features to [0, 1]
3. Elbow method to choose k (typically k=5)
4. K-means fit → spatial and feature-space cluster plots
5. Cross-reference cluster membership with `stc_*` labels from `challenge_1min_labels.nc`

The main submission notebook (`OpenChallangeNotebook-Ch1-EarthCARE_Cloud_Aerosols_Interactions.ipynb`) contains the complete end-to-end analysis with narrative.

## Notebook Overview

| Notebook | Purpose |
|----------|---------|
| `OpenChallangeNotebook-Ch1-*.ipynb` | Primary submission — full analysis with narrative |
| `merger.ipynb` / `merger_EP.ipynb` | Data loading, merging, resampling → NetCDF |
| `kmeans.ipynb` / `kmeans_EP.ipynb` | K-means clustering + visualization |
| `kmeans-labels.ipynb` | Extended clustering including `stc_*` label variables |
| `atl_ald_2a.ipynb` | ATLID aerosol product EDA |
| `cpr_cld_2a.ipynb` / `_EP` | Cloud radar product EDA |
| `ac__tc__2b.ipynb` / `_EP` | Synergetic classification product EDA |
| `atl_tc_2a_Antarctica_SLC.ipynb` | Aerosol lidar for Antarctica |
| `cpr_fmr_2a_ITA_radarDPC.ipynb` | Radar comparison over Italy with DPC data |

## Intermediate Data Files

Notebooks write NetCDF files to the root directory:
- `challenge_1min_numerical.nc` — numerical features at 1-min resolution
- `challenge_1min_labels.nc` — classification labels at 1-min resolution
- `challenge_1min_complete.nc` — merged complete dataset
- Regional variants use suffixes (e.g., `_EP` for East Pacific, `_R1`/`_R2` for Antarctica)
