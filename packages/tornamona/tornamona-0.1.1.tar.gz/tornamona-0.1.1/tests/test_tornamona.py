#!/usr/bin/env python

"""Tests for `tornamona` package."""

import pytest

from click.testing import CliRunner

from tornamona import nisra
from tornamona import cli

import pandas as pd


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_nisra_smoke():
    v = nisra.WeeklyDeaths().get().clean()
    assert v.data.shape[1] == 10, 'Should be 10 Columns Wide'
    assert any(v.data['Week Start']==pd.to_datetime('2004-02-01')) == False, 'Found crazy 2004 date'
    assert v.data.dtypes['Week Start'] == '<M8[ns]', 'Datetime column inference broken'

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'tornamona.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
