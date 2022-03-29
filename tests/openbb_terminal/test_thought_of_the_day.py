""" thought_of_the_day.py tests """
import unittest
from unittest import mock

# pylint: disable=unused-import
from tests.helpers.tools import (  # noqa: F401
    parameterize_from_file,
    pytest_generate_tests,
)
from openbb_terminal import thought_of_the_day

assertions = unittest.TestCase("__init__")


class TestThoughtOfTheDay:
    @parameterize_from_file(
        "test_get_urls",
        "../../tests/openbb_terminal/yaml/test_thought_of_the_day/thought_of_the_day.yaml",
    )
    def test_get_urls(self, urls):
        a_totd = thought_of_the_day.ThoughtOfTheDay(urls)

        assertions.assertEqual(a_totd.get_urls(), urls)

    @mock.patch("openbb_terminal.thought_of_the_day.requests")
    @parameterize_from_file(
        "test_get_metadata",
        "../../tests/openbb_terminal/yaml/test_thought_of_the_day/thought_of_the_day.yaml",
    )
    def test_get_metadata(
        self, mock_request_get, urls, mock_goodreads_page, expected_result
    ):
        mock_request_get.get().text = mock_goodreads_page

        a_totd = thought_of_the_day.ThoughtOfTheDay(urls)

        meta = a_totd.get_metadata(list(urls.keys())[0])

        assertions.assertEqual(meta, expected_result)
