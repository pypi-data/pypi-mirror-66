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

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from datetime import datetime

metadata = MetaData()

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('fullname', String(50)),
)

addresses = Table('addresses', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('users.id')),
    Column('email_address', String(50), nullable=False)
)

roles = Table('roles', metadata,
    Column('role_id', Integer, primary_key=True, autoincrement=True),
    Column('role_name', String, nullable=False, unique=True),
    Column('role_display_name', String, nullable=True),
    Column('role_description', String, nullable=True),
    Column('role_created_at', DateTime),
    Column('role_updated_at', DateTime)
)

test_type_table = Table('_test_table', metadata,
    Column('id', Integer, primary_key=True),
    Column('t_a', Integer(), index=True),
    Column('t_datetime', DateTime, default=datetime(2020, 4, 16), onupdate=datetime.now, index=True),
)
