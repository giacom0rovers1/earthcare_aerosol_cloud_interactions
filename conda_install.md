conda create -p earthcare_env -c conda-forge numpy scipy xarray pandas h5py h5netcdf netcdf4 cftime zarr pystac-client fsspec matplotlib tqdm aiohttp requests ipykernel
source activate /home/jovyan/earthcare_env
python -m ipykernel install --user --name earthcare --display-name "Python (earthcare_kernel)"