import pytest

from .model import roles
from datetime import datetime

ROLES = [
    {
        'role_name': 'administrator',
        'role_display_name': 'Super Administrator',
        'role_description': 'Super Administrator',
        # 'created_at': datetime(2018, 1, 1),
        # 'updated_at': datetime(2019, 1, 1)
    }
]

@pytest.mark.asyncio
async def test_pool_basic(pool):
    async with pool.acquire() as con:
        for sample_item in ROLES:
            query = roles.insert(sample_item)
            print(await pool.fetchval(query))
