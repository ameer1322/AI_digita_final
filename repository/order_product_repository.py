from repository.database import database


async def get_order_products():
    query = """
    SELECT * FROM order_product
    """
    return await database.fetch_all(query)