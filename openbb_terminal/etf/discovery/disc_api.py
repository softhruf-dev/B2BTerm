"""Discover context API."""
import os
from openbb_terminal.helper_classes import ModelsNamespace as _models

# flake8: noqa
# pylint: disable=unused-import

# Context menus
from openbb_terminal.etf.discovery.wsj_view import show_top_mover as mover

# Models
models = _models(os.path.abspath(os.path.dirname(__file__)))
