from repository.database import database


async def add_to_favorites(user_id:int, product_id:int):
    query = """
    INSERT INTO favorites(user_id, product_id)
    VALUES(:user_id, :product_id)
    """
    values = {"user_id":user_id, "product_id":product_id}
    result = await database.execute(query,values)
    return "created"

async def remove_from_favorites(user_id:int, product_id:int):
    query = """
    DELETE FROM favorites
    WHERE user_id = :user_id AND product_id = :product_id
    """
    values = {"user_id":user_id, "product_id": product_id}
    result = await database.execute(query, values)
    return "deleted"

async def get_user_favorites_by_product_id(product_id:int, user_id:int):
    query = """
    SELECT * FROM favorites
    WHERE user_id = :user_id AND product_id = :product_id
    """
    values = {"user_id": user_id, "product_id": product_id}
    result = await database.fetch_one(query,values)
    return result

async def get_user_favorites(user_id:int):
    query = """
    SELECT * FROM favorites
    JOIN products ON favorites.product_id = products.product_id
    WHERE user_id = :user_id 
    """
    values = {"user_id":user_id}
    result = await database.fetch_all(query,values)
    return result