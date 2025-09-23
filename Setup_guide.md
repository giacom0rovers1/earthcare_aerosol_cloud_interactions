# Setup guide on a new PAL account

In the home folder, download the repository:

```git clone https://github.com/giacom0rovers1/earthcare_aerosol_cloud_interactions.git```

Create a new Anaconda environment with the required packages:

```conda create -p ./conda_envs/earthcare -c conda-forge numpy scipy xarray pandas h5py h5netcdf netcdf4 cftime zarr pystac-client fsspec matplotlib tqdm aiohttp requests ipykernel seaborn scikit-learn```

Activate the new environment:

```source activate /home/jovyan/conda_envs/earthcare```

Create a Jupyter kernel inside the environment, in order to get the installed packages in Jupyterlab:

```python -m ipykernel install --user --name earthcare --display-name "Python (earthcare_kernel)"```

