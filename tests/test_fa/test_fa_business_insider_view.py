""" fundamental_analysis/business_insider_api.py tests """
import unittest

import vcr

from gamestonk_terminal.stocks.fundamental_analysis.business_insider_view import (
    management,
)
from tests.helpers import check_print


class TestFaBusinessInsiderApi(unittest.TestCase):
    @check_print(assert_in="PLTR")
    @vcr.use_cassette(
        "tests/cassettes/test_fa/test_fa_business/test_management.yaml",
        record_mode="new_episodes",
    )
    def test_management(self):
        management([], "PLTR")
