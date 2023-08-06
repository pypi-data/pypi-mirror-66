# Vincenty nearest neighbor search using CUDA
Nearest neighbor search algorithm on Earth's surface that runs on a GPU and uses [Vincenty's formula](https://en.wikipedia.org/wiki/Vincenty%27s_formulae)

## Application
Nearest Neighbour Search is the **key component of location data analysis**:
- Nearest Neighbour Index is based on measuring distances between points
- Both **global** pattern analysis algorithms (Global Moran’s I, Getis-Ord General G), as well as **local** pattern analysis algorithms (Anselin Local Moran's I, Getis Ord GI *) with the **k-nn approach** to define neighbours are based on measuring distances between points

Using Vincenty’s formula allows performing location analysis on **any location using geographic coordinates**.

[Presentation slides](https://docs.google.com/presentation/d/1c0-9hQVlZoordzm1gZ9uKQJVqDyZQ9lZQe-SBEo-lwE/edit?usp=sharing)

## Requirements
- CUDA-enabled GPU with compute capability 2.0 or above with an up-to-data Nvidia driver.
- [CUDA toolkit](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html])

## Installation
```
pip install vincenty-cuda-nns
```

## Usage example
```python
import geopandas as gpd  # here just for example
import numpy as np
from vincenty_cuda_nns import CudaTree

df = gpd.read_file('points.geojson')

# data is array of points like [longitude, latitude]
points = np.stack(df['geometry']).astype(np.float32)

# build tree for the data
cuda_tree = CudaTree(points, leaf_size=4)

# query over the tree for tree nearest neighbors (+1 for itself)
distances, indices = cuda_tree.query(points, n_neighbors=4)

# you can also find distances from andother dataset
from_points = (np.random.random((100, 2)) * 180) - 90

distances, indices = cuda_tree.query(from_points)
```
