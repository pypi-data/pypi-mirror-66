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


@pytest.fixture
async def apgsa_conn():
    """
    Create an apgsa connection for each test case.

    """
    conn = await apgsa.connect(user='test_user', password='test_pass',
                                database='test_db', host='127.0.0.1')

    yield conn
    await conn.close()


@pytest.fixture
async def conn(apgsa_conn):
    yield apgsa_conn

    # teardown table users
    await apgsa_conn.execute(users.delete())

ROWS_ADDRESS = [
    {'user_id': 1, 'email_address': 'jack@yahoo.com'},
    {'user_id': 1, 'email_address': 'jack@msn.com'},
    {'user_id': 2, 'email_address': 'www@www.org'},
    {'user_id': 2, 'email_address': 'wendy@aol.com'},
]

@pytest.mark.asyncio
async def test_executing_multiple_statements(conn):
    # ins = users.insert()
    # query = str(ins)

    ins = addresses.insert().values(ROWS_ADDRESS)
    # Test a sample of the SQL this construct produces
    query_literal = await conn.execute(ins)
    # assert query == 'sa'
    assert query_literal == 'apgsa'
