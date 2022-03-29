import pytest

from openbb_terminal.cryptocurrency.onchain import blockchain_view


@pytest.mark.vcr
@pytest.mark.record_stdout
def test_display_btc_circulating_supply(mocker):
    # MOCK VISUALIZE_OUTPUT
    mocker.patch(target="openbb_terminal.helper_classes.TerminalStyle.visualize_output")

    blockchain_view.display_btc_circulating_supply(1_601_596_800, 1_641_573_787, "")


@pytest.mark.vcr
@pytest.mark.record_stdout
def test_display_btc_confirmed_transactions(mocker):
    # MOCK VISUALIZE_OUTPUT
    mocker.patch(target="openbb_terminal.helper_classes.TerminalStyle.visualize_output")
    blockchain_view.display_btc_confirmed_transactions(1_601_596_800, 1_641_573_787, "")
