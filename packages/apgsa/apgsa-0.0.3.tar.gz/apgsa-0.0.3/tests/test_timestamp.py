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

from .model import roles
from sqlalchemy.sql import select, insert
from datetime import datetime

ROLES = [
    {
        # 'role_name': 'superadministrator',
        'role_display_name': 'Super Administrator',
        'role_description': 'Super Administrator',
        # 'created_at': '20180102',
        # 'updated_at': '20199392'
    }
]

@pytest.mark.asyncio
async def test_timestamp(conn):
    """
    Create a row

    """
    ins_role = roles.insert().values(ROLES)
    # time = datetime.now()
    query_compiled = conn._literalquery(ins_role)
    # query_compiled = str(ins_role)

    assert query_compiled == 'INSERT 0 1'

    # """
    # Fetch a row

    # """
    # query = select([roles])
    # row = await conn.fetchrow(query)
    # assert row == 1
