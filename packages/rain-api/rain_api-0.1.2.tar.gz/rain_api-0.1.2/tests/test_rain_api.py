#!/usr/bin/env python

"""Tests for `rain_api` package."""
import pytest

from click.testing import CliRunner

from rain_api import cli


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


def test_command_line_interface_step_1():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_command_line_interface_step_2():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli, ['create'])
    assert help_result.exit_code == 0
    assert 'Initialized the service.' in help_result.output


def test_command_line_interface_step_3():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli, ['start'])
    assert help_result.exit_code == 0
    assert 'Initialized the service.' in help_result.output
