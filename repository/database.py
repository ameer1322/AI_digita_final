from config.config import config
from databases import Database

database = Database(config.DATABASE_URL)