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

import pytest

from .model import test_type_table
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.dialects import postgresql

SAMPLE_DATA = [
    {
        't_a': 1,
        # 't_datetime': datetime(2020, 4, 16)
    },
]

@pytest.mark.asyncio
async def test_execute(pg):
    """
    TEST asyncpg raw api: execute
    """
    # SQL style
    await pg.execute("INSERT INTO _test_table (t_a) VALUES ($1), ($2)", 10, 20)
    rows = await pg.fetch("SELECT * from _test_table;")
    assert len(rows) == 2

    # SA style
    stmt = test_type_table.insert().values(SAMPLE_DATA)
    await pg.execute(stmt)
    rows = await pg.fetch(select([test_type_table]))
    assert rows[2]['t_datetime'] == datetime(2020, 4, 16)
