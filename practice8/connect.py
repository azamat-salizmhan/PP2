import psycopg2
from config import params

def connect():
    """ PostgreSQL мәліметтер базасына қосылу """
    conn = None
    try:
        
        print('PostgreSQL базасына қосылуда...')
        conn = psycopg2.connect(**params)
        
        
        cur = conn.cursor()
        
        print('База нұсқасы:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        
        cur.close()
        return conn 
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Қосылу кезінде қате шықты: {error}")
        return None

if __name__ == '__main__':
    connect()