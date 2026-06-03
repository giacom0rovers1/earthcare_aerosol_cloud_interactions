#!/usr/bin/env python
"""Check which data files the analysis pipeline needs and which are present.

Run this right after cloning on the MAAP PAL (or locally) to see what still
has to be regenerated before the clustering / report notebooks can run:

    python check_data.py

The .nc files are git-ignored and are *not* part of the repository — they are
produced on the MAAP JupyterHub by the EDA and merger notebooks (which need a
bearer token in ``token.txt``). This script never downloads anything; it only
reports presence and points at the notebook that produces each missing file.
"""
from __future__ import annotations

import os

# Per region: suffix used in the merged filenames, the aerosol filename, the
# notebook that produces that aerosol file, and a human-readable label.
# WP has no suffix; WP+EP aerosols both come from the single atl_ald_2a.ipynb.
REGIONS = [
    ("West Pacific", "", "aot_resampled_wp.nc", "atl_ald_2a.ipynb"),
    ("East Pacific", "_EP", "aot_resampled_ep.nc", "atl_ald_2a.ipynb"),
    ("Antarctica", "_AN", "aot_resampled_an.nc", "atl_ald_2a_AN.ipynb"),
]

# file -> notebook that produces it ({s} = region suffix, {aot} = aot file,
# {nb} = notebook suffix, {aot_nb} = aerosol notebook)
RAW = [
    ("AC__TC__2B_1s{s}.nc", "ac__tc__2b{nb}.ipynb"),
    ("CPR_CLD_2A_1s{s}.nc", "cpr_cld_2a{nb}.ipynb"),
    ("{aot}", "{aot_nb}"),
]
MERGED = [
    ("challenge_1min_numerical{s}.nc", "merger{nb}.ipynb"),
    ("challenge_1min_complete{s}.nc", "merger{nb}.ipynb"),
]

OK, MISSING = "[ok]  ", "[ --] "


def nb_suffix(suffix: str) -> str:
    """EDA/merger notebooks use '' for WP, '_EP'/'_AN' otherwise."""
    return suffix  # happens to match the filename suffix in this project


def report() -> bool:
    here = os.path.dirname(os.path.abspath(__file__))
    all_present = True

    token = os.path.join(here, "token.txt")
    print("MAAP token:")
    print(f"  {OK if os.path.exists(token) else MISSING}token.txt "
          f"(needed only to (re)generate data on the PAL)")
    print()

    for label, suffix, aot, aot_nb in REGIONS:
        print(f"{label}  (suffix '{suffix or '<none>'}')")
        nb = nb_suffix(suffix)
        for group_name, group in (("raw products", RAW), ("merged datasets", MERGED)):
            print(f"  {group_name}:")
            for fname_tpl, producer_tpl in group:
                fname = fname_tpl.format(s=suffix, aot=aot)
                producer = producer_tpl.format(nb=nb, aot_nb=aot_nb)
                present = os.path.exists(os.path.join(here, fname))
                all_present &= present
                hint = "" if present else f"  -> run {producer}"
                print(f"    {OK if present else MISSING}{fname}{hint}")
        print()

    if all_present:
        print("All data files present - clustering and report.ipynb can run.")
    else:
        print("Some files are missing. Regenerate them on the MAAP PAL in order:")
        print("  EDA notebooks (need token.txt) -> merger{,_EP,_AN} -> kmeans / report")
    return all_present


if __name__ == "__main__":
    raise SystemExit(0 if report() else 1)
