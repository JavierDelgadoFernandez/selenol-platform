# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Test app module."""

import os
import tempfile
from importlib import import_module

from click.testing import CliRunner
from mock import patch
from pkg_resources import EntryPoint
from sqlalchemy import MetaData, create_engine

from selenol_platform import config
from selenol_platform.cli import create_db, create_fixtures, run


class ImportLibEntryPoint(EntryPoint):
    """Specilization of EntryPoint to load custom strings import."""

    def load(self):
        """Import module using importlib library."""
        return getattr(import_module(self.module_name), *self.attrs)


def _mock_entry_points(group=None):
    """Mocking entrypoints funtion."""
    data = {
        'selenol.services': [
            ImportLibEntryPoint(
                'Test_service', 'demo.service', attrs=('TestService',)),
        ],
        'selenol.fixtures': [
            ImportLibEntryPoint(
                'Test_fixture', 'demo.fixtures', attrs=('create_test',)),
        ],
    }
    names = data.keys() if group is None else [group]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


@patch('pkg_resources.iter_entry_points', _mock_entry_points)
def test_fixtures_execution():
    """Test the execution of the fixtures."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        orinal_path = os.getcwd()
        os.chdir(tmpdir)
        result = runner.invoke(create_db, [
            '-c', config.SELENOL_DEFAULT_DATABASE_CONNECTION])
        assert result.exit_code == 0

        # Due to we don't have access to the class, we have to infer it.
        engine = create_engine(config.SELENOL_DEFAULT_DATABASE_CONNECTION)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        test_table = metadata.tables['test_table']

        assert engine.scalar(test_table.count()) == 0
        result = runner.invoke(create_fixtures, [
            '-c', config.SELENOL_DEFAULT_DATABASE_CONNECTION])
        assert result.exit_code == 0
        assert engine.scalar(test_table.count()) == 1
        os.chdir(orinal_path)


@patch('pkg_resources.iter_entry_points', _mock_entry_points)
def test_db_creation():
    """Test the CLI for the database creation."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        result = runner.invoke(create_db, [
            '-c', config.SELENOL_DEFAULT_DATABASE_CONNECTION])
        assert result.exit_code == 0

        engine = create_engine(config.SELENOL_DEFAULT_DATABASE_CONNECTION)
        assert engine.has_table('test_table')


@patch('pkg_resources.iter_entry_points', _mock_entry_points)
@patch('selenol_platform.pool.SelenolPool.serve', lambda pool: None)
def test_app_run():
    """Test the execution of the application."""
    runner = CliRunner()
    result = runner.invoke(run)
    assert result.exit_code == 0
