from orator import DatabaseManager
from orator import Model
from dotenv import load_dotenv
import os

load_dotenv()
mysql_config = { 
    'mysql': {
        'driver': 'mysql',
        'host': os.environ.get('DB_HOST'),
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
    }
}
db = DatabaseManager(mysql_config)
db.connection().enable_query_log()
Model.set_connection_resolver(db)
