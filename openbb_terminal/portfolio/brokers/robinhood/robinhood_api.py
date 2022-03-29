"""Robinhood API."""
import os
from openbb_terminal.helper_classes import ModelsNamespace as _models

# flake8: noqa
# pylint: disable=unused-import

# Context menus
from openbb_terminal.portfolio.brokers.robinhood.robinhood_view import (
    display_holdings as holdings,
)
from openbb_terminal.portfolio.brokers.robinhood.robinhood_view import (
    display_historical as historical,
)

# Models
models = _models(os.path.abspath(os.path.dirname(__file__)))
