# MIT License

# Copyright (c) 2020 Kelvin Gao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncpg

from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.dml import Insert as InsertObject, Update as UpdateObject
from sqlalchemy.sql.ddl import DDLElement

from sqlalchemy.dialects import postgresql
from .dialect import LiteralDialect

def get_dialect(**kwargs):
    dialect = postgresql.dialect(paramstyle='pyformat', **kwargs)

    return dialect


def compile_query(query, dialect=get_dialect(), inline=False):
    if isinstance(query, str):
        return query, None

class PGConnection(asyncpg.Connection):
    """
    A representation of a database session.

    """
    async def execute(self, query: str, *args, timeout: float = None) -> str:
        """
        Overwrite execute function with dialect wedged.

        """
        # postgresql dialect wedged
        if not isinstance(query, str):
            query = self._literalquery(query)

        self._check_open()

        if not args:
            return await self._protocol.query(query, timeout)

        _, status, _ = await self._execute(query, args, 0, timeout, True)
        return status.decode()

    async def _execute(self, query, args, limit, timeout, return_status=False):
        """
        Overwrite _execute function with dialect wedged.

        """
        if not isinstance(query, str):
            query = self._literalquery(query)

        with self._stmt_exclusive_section:
            result, _ = await self.__execute(
                query, args, limit, timeout, return_status=return_status)
        return result

    async def __execute(self, query, args, limit, timeout,
                        return_status=False):
        """
        Double underscore prefix causes Python to rewrite the attribute name.

        """
        executor = lambda stmt, timeout: self._protocol.bind_execute(
            stmt, args, '', limit, return_status, timeout)
        timeout = self._protocol._get_timeout(timeout)
        return await self._do_execute(query, executor, timeout)

    def _literalquery(self, query, literal_binds=True):
        import sqlalchemy.orm

        _dialect = LiteralDialect(
            paramstyle='pyformat', implicit_returning=True)

        if isinstance(query, sqlalchemy.orm.Query):
            query = query.statement

        literal = query.compile(
            dialect=_dialect,
            compile_kwargs={'literal_binds': literal_binds},
        ).string

        return literal


async def connect(dsn=None, *,
                  host=None, port=None,
                  user=None, password=None, passfile=None,
                  database=None,
                  loop=None,
                  timeout=60,
                  statement_cache_size=100,
                  max_cached_statement_lifetime=300,
                  max_cacheable_statement_size=1024 * 15,
                  command_timeout=None,
                  ssl=None,
                  connection_class=PGConnection,
                  server_settings=None):
    """
    Overwrite connect function with PGConnection class.

    """
    return await asyncpg.connect(loop=loop, connection_class=connection_class,
        dsn=dsn, host=host, port=port, user=user, password=password, passfile=passfile,
        database=database, timeout=timeout, statement_cache_size=statement_cache_size,
        max_cached_statement_lifetime=max_cached_statement_lifetime,
        max_cacheable_statement_size=max_cacheable_statement_size,
        command_timeout=command_timeout, ssl=ssl, server_settings=server_settings)
