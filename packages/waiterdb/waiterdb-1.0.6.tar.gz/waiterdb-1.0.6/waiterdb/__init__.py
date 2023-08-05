# Copyright 2015 Lukas Lalinsky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from waiterdb import errors
from waiterdb.avatica import AvaticaClient
from waiterdb.connection import Connection
from waiterdb.errors import *  # noqa: F401,F403


__all__ = ['connect', 'apilevel', 'threadsafety', 'paramstyle'] + errors.__all__

apilevel = "2.0"
"""
This module supports the `DB API 2.0 interface <https://www.python.org/dev/peps/pep-0249/>`_.
"""

threadsafety = 1
"""
Multiple threads can share the module, but neither connections nor cursors.
"""

paramstyle = 'qmark'


def connect(url, max_retries=None, **kwargs):
    """Connects to a Phoenix query server.

    :param url:
        URL to the Phoenix query server, e.g. ``http://localhost:8765/``

    :param max_retries:
        The maximum number of retries in case there is a connection error.
        
    :param autocommit:
        Switch the connection to autocommit mode.

    :param readonly:
        Switch the connection to readonly mode.

    :param cursor_factory:
        If specified, the connection's :attr:`~waiterdb.connection.Connection.cursor_factory` is set to it.

    :returns:
        :class:`~waiterdb.connection.Connection` object.
    """
    client = AvaticaClient(url, max_retries=max_retries)
    client.connect()
    return Connection(client, **kwargs)
