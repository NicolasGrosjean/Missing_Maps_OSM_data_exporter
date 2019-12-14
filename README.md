# Missing Maps OSM data exporter
> Tool to export OSM data for Missing Maps projects

## Installation

Download or clone this repository.

### Python
I recommend you to install a Python environment with conda or virtualenv.

For example with conda, 
[download and install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Create a conda environment
```
conda create -n mm_osm python=3.7
```

Activate the conda environment
```
activate mm_osm
```

Install the packages with the following commands
```
conda install geojson requests
```

## Usage

Activate the conda environment
```
activate mm_osm
```

TODO

## Tests

Go to the tests directory and run unittest
```
cd tests
python -m unittest discover
```

## Licence

The project have an Apache-2.0 licence because of the inclusion of
[overpass](https://github.com/mvexel/overpass-api-python-wrapper) which has this licence.