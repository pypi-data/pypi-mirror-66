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
import apgsa

from .model import users, addresses
from sqlalchemy.sql import select

@pytest.mark.asyncio
async def test_selecting(conn):
    """
    SELECT all rows, first row.

    """
    # fetch all records
    query = select([users])
    records = await conn.fetch(query)

    assert records[0]['id'] == 1
    assert records[1]['id'] == 2
    assert records[0]['name'] == 'jack'
    assert records[1]['name'] == 'wendy'

    # fetch first row
    row = await conn.fetchrow(query)

    assert row['id'] == 1
    assert row['name'] == 'jack'

@pytest.mark.asyncio
async def test_selecting_specific_columns(conn):
    """
    SELECT rows with specific columns.

    """
    query = select([users.c.name, users.c.fullname])

    records = await conn.fetch(query)

    assert records[0]['name'] == 'jack'
    assert records[1]['name'] == 'wendy'
    assert records[0]['fullname'] == 'Jack Jones'
    assert records[1]['fullname'] == 'Wendy Williams'

@pytest.mark.asyncio
async def test_selecting_from_tables(conn):
    """
    SELECT all rows FROM distinct tables.

    """
    query = select([users, addresses])
    records = await conn.fetch(query)

    # (1, u'jack', u'Jack Jones', 1, 1, u'jack@yahoo.com')
    # (1, u'jack', u'Jack Jones', 2, 1, u'jack@msn.com')
    # (1, u'jack', u'Jack Jones', 3, 2, u'www@www.org')
    # (1, u'jack', u'Jack Jones', 4, 2, u'wendy@aol.com')
    # (2, u'wendy', u'Wendy Williams', 1, 1, u'jack@yahoo.com')
    # (2, u'wendy', u'Wendy Williams', 2, 1, u'jack@msn.com')
    # (2, u'wendy', u'Wendy Williams', 3, 2, u'www@www.org')
    # (2, u'wendy', u'Wendy Williams', 4, 2, u'wendy@aol.com')

    assert records[0][0] == 1  # Record id
    assert records[0]['name'] == 'jack'
    assert records[0]['fullname'] == 'Jack Jones'
    assert records[0]['id'] == 1
    assert records[0]['user_id'] == 1
    assert records[0]['email_address'] == 'jack@yahoo.com'

@pytest.mark.asyncio
async def test_selecting_join_tables(conn):
    """
    SELECT rows FROM distinct tables with WHERE clause.

    """
    query = select([users, addresses]).where(users.c.id == addresses.c.user_id)
    records = await conn.fetch(query)

    assert len(records) == 4

    # (1, u'jack', u'Jack Jones', 1, 1, u'jack@yahoo.com')
    # (1, u'jack', u'Jack Jones', 2, 1, u'jack@msn.com')
    # (2, u'wendy', u'Wendy Williams', 3, 2, u'www@www.org')
    # (2, u'wendy', u'Wendy Williams', 4, 2, u'wendy@aol.com')

    assert records[2]['user_id'] == 2
