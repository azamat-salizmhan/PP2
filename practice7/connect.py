# connect.py
import psycopg2
import config

def get_connection():
    """Connect to the PostgreSQL database server"""
    try:
        conn = psycopg2.connect(
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.password
        )
        print(f"Successfully connected to the database on port {config.port}.")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection Error: {error}")
        return None