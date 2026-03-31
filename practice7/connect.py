import psycopg2
from config import DB_CONFIG


def get_connection():
    """Create and return a new database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Could not connect to database: {e}")
        raise


def create_table():
    """Create the phonebook table if it does not exist."""
    sql = """
        CREATE TABLE IF NOT EXISTS phonebook (
            id        SERIAL PRIMARY KEY,
            firstname VARCHAR(100) NOT NULL,
            lastname  VARCHAR(100),
            phone     VARCHAR(20)  NOT NULL UNIQUE
        );
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        print("[OK] Table 'phonebook' is ready.")
    finally:
        conn.close()