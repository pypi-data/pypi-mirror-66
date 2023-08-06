
# ipyaliplayer

[![Build Status](https://travis-ci.org/boyuai/ipyaliplayer.svg?branch=master)](https://travis-ci.org/boyuai/ipyaliplayer)
[![codecov](https://codecov.io/gh/boyuai/ipyaliplayer/branch/master/graph/badge.svg)](https://codecov.io/gh/boyuai/ipyaliplayer)


A Custom Jupyter Widget Library

## Installation

You can install using `pip`:

```bash
pip install ipyaliplayer
```

Or if you use jupyterlab:

```bash
pip install ipyaliplayer
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipyaliplayer
```

## Development

```bash
docker run --rm -it -p 8888:8888 -v $(pwd):/home/jovyan/ipyaliplayer jupyter/minimal-notebook bash
```

```bash
pip install -e ".[test, examples]"
jupyter nbextension install --sys-prefix --symlink --overwrite --py ipyaliplayer
jupyter nbextension enable --sys-prefix --py ipyaliplayer
jupyter notebook
```

[http://localhost:8888](http://localhost:8888)
