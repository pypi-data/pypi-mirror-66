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

from apgsa import PG
from sqlalchemy.engine import create_engine

from .model import metadata

DSN = 'postgresql://test_user:test_pass@localhost/test_db'


@pytest.fixture
async def pg():
    pg = PG(DSN, metadata)
    try:
        pg.create_all()
        await pg.init_pool()
        yield pg
    finally:
        pg.drop_all()


# @pytest.fixture
# async def conn(pg):
#     """This fixture creates table before each test function in this module and,
#     drops it after, so that each test gets a clean table.
#     """
#     try:
#         pool = await pg.init_pool()
#         conn = await pool.acquire()
#         yield conn
#     finally:
#         pool.release(conn)
