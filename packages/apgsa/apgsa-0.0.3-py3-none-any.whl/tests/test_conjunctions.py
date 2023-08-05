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
from sqlalchemy.sql import select, and_, or_, not_

@pytest.mark.asyncio
async def test_conjunctions(conn):
    """
    SELECT all rows, first row.

    """
    s = select([(users.c.fullname +
                    ", " + addresses.c.email_address).label('title')]).\
            where(
                and_(
                    users.c.id == addresses.c.user_id,
                    users.c.name.between('m', 'z'),
                    or_(
                        addresses.c.email_address.like('%@aol.com'),
                        addresses.c.email_address.like('%@msn.com')
                    )
                )
            )

    records = await conn.fetch(s)

    # <Record title='Wendy Williams, wendy@aol.com'>
    assert records[0]['title'] == 'Wendy Williams, wendy@aol.com'
