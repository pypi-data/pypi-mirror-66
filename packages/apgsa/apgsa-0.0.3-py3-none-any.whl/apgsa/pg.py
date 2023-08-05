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

from sqlalchemy import MetaData
from sqlalchemy import func
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.dml import Insert as InsertObject, Update as UpdateObject
from sqlalchemy.sql.ddl import DDLElement
from sqlalchemy.engine import create_engine
from sqlalchemy.dialects import postgresql

class NotInitializedError(Exception):
    pass


class PG:
    """
    A wrapper around asyncpg for use with sqlalchemy core.

    """
    RequestTimeout = None

    _dialect = postgresql.dialect(paramstyle='pyformat')

    __slot__ = ('_dsn', '_metadata', '_engine', '_pool')

    def __init__(self, dsn: str, metadata: MetaData):
        """
        Bind metadata to sqlalchemy engine.

        """

        self._dsn = dsn
        self._metadata = metadata
        self._metadata.bind = create_engine(self._dsn)

    def __repr__(self) -> str:
        return self._dsn

    __str__ = __repr__

    @property
    def pool(self):
        if not self._pool:
            raise NotInitializedError('pg.init_pool() needs to be called '
                                      'before you can make queries')
        else:
            return self._pool

    # ---------------------------------------
    async def init_pool(self):
        # connect to the pool
        self._pool = await asyncpg.create_pool(self._dsn)
        return self

    async def close_pool(self):
        """
        Gracefully close all connections in the pool,
        it is advisable to use asyncio.wait_for() to set a timeout.
        """

        if not self._pool:
            return

        await self._pool.close()

    def execute_defaults(self, query):
        if isinstance(query, InsertObject):
            attr_name = 'default'
        elif isinstance(query, UpdateObject):
            attr_name = 'onupdate'
        else:
            return query

        # query.parameters could be a list in a multi row insert
        if isinstance(query.parameters, list):
            for param in query.parameters:
                self._execute_default_attr(query, param, attr_name)
        else:
            query.parameters = query.parameters or {}
            self._execute_default_attr(query, query.parameters, attr_name)
        return query

    def _execute_default_attr(self, query, param, attr_name):
        for col in query.table.columns:
            attr = getattr(col, attr_name)
            if attr and param.get(col.name) is None:
                if attr.is_sequence:
                    param[col.name] = func.nextval(attr.name)
                elif attr.is_scalar:
                    param[col.name] = attr.arg
                elif attr.is_callable:
                    param[col.name] = attr.arg({})

    def _compile_query(self, query, inline=False):
        """
        Render a sqlalchemy sql statement.

        """
        if isinstance(query, str):
            return query, ()

        elif isinstance(query, DDLElement):
            compiled = query.compile(dialect=self._dialect)
            new_query = compiled.string
            return new_query, ()

        elif isinstance(query, ClauseElement):
            query = self.execute_defaults(query)  # adjust default values for Insert/Update

            compiled = query.compile(dialect=self._dialect)
            compiled_params = sorted(compiled.params.items())

            mapping = {key: '$' + str(i)
                   for i, (key, _) in enumerate(compiled_params, start=1)}
            new_query = compiled.string % mapping

            processors = compiled._bind_processors
            new_params = [processors[key](val) if key in processors else val
                        for key, val in compiled_params]

            if inline:
                return new_query
            return new_query, new_params

    async def execute(self, query, *args, timeout=RequestTimeout):
        query, compiled_args = self._compile_query(query)
        args = compiled_args or args
        return await self.pool.execute(query, *args, timeout=timeout)

    async def executemany(self, command: str, *args, timeout=RequestTimeout):
        command, compiled_args = self._compile_query(command)
        args = compiled_args or args
        return await self.pool.executemany(command, *args, timeout=timeout)

    async def fetch(self, query, *args, timeout=RequestTimeout) -> list:
        query, compiled_args = self._compile_query(query)
        args = compiled_args or args
        return await self.pool.fetch(query, *args, timeout=timeout)

    async def fetchval(self, query, *args, column=0, timeout=RequestTimeout):
        query, compiled_args = self._compile_query(query)
        args = compiled_args or args
        return await self.pool.fetchval(query, *args, column=column, timeout=timeout)

    async def fetchrow(self, query, *args, timeout=RequestTimeout):
        query, compiled_args = self._compile_query(query)
        args = compiled_args or args
        return await self.pool.fetchrow(query, *args, timeout=timeout)

    def create_all(self):
        """
        Create tables.

        """
        self._metadata.create_all()

    def drop_all(self):
        """
        Drop tables.

        """
        self._metadata.drop_all()
