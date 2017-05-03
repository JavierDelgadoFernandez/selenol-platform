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

"""Test pool module."""

import logging
from unittest.mock import patch

from selenol_platform.pool import SelenolPool, service_manager


class ListHandler(logging.Handler):
    """List handler for logging."""

    def __init__(self, log_level=logging.INFO):
        """Default constructor.

        :param log_level: Log level.
        """
        super(ListHandler, self).__init__()
        self.level = log_level
        self.records = []
        self.filters = []
        self.lock = None

    def emit(self, record):
        """Store an event inside the records list.

        :param record: Record to be stored.
        """
        self.records.append(record)


def test_service_manager_exception():
    """Test the service manager using a wrong service."""
    list_handler = ListHandler()
    logging.getLogger().addHandler(list_handler)
    assert len(list_handler.records) == 0

    class DummyService(object):
        """Selenol dummy service."""
        def __init__(*args):
            """Default constructor."""

        def run(self):
            """"Run method implenetation throwing an exception."""
            raise ArithmeticError()
    service_manager(DummyService)
    assert len(list_handler.records) == 1
    assert isinstance(list_handler.records[0].msg, ArithmeticError)


@patch('threading.Thread.start', lambda thread: None)
def test_selenol_pool():
    """Test SelenolPool class default behavior."""
    class DummyService(object):
        """Selenol dummy service."""
        def run(self):
            """"Run method implementation doing anything."""

    pool = SelenolPool([DummyService])

    assert len(pool.processess) == 0
    assert len(pool.services) == 1

    pool.serve()

    assert len(pool.processess) == 1
    assert len(pool.services) == 1
