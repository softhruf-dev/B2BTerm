#!/bin/bash

source $(poetry env info --path)/bin/activate

pip install -e jupyterlab/gst
pip install -e jupyterlab/gst-settings
pip install -e jupyterlab/documentation
jupyter-labextension install jupyterlab/gst
jupyter-labextension install jupyterlab/gst-settings
jupyter-labextension install jupyterlab/documentation
