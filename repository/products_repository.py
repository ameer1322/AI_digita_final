from typing import Optional, List

import json
from repository.database import database

async def get_products():
    query = """
        SELECT * FROM products
        WHERE quantity > 0
    """
    return await database.fetch_all(query)

