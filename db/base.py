from config import config
from pony.orm import Database, sql_debug
import cloudinary

cloudinary.config(
    cloud_name=config.CLOUD_NAME, api_key=config.API_KEY, api_secret=config.API_SECRET
)

db = Database()
db.bind(provider=config.DB_PROVIDER, filename=config.DB_NAME, create_db=True)

if config.DEBUG:
    sql_debug(True)
