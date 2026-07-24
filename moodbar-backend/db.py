import os

import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

# la BDD est distante (Railway) : une connexion par requête coûte ~2s de handshake réseau.
# un pool ouvert une fois au démarrage évite ce coût sur chaque vote.
_pool = pooling.MySQLConnectionPool(
    pool_name="moodbar_pool",
    pool_size=5,
    pool_reset_session=False,
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "moodbar"),
)


def get_connection():
    return _pool.get_connection()
