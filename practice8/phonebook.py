import psycopg2
from config import params 

def manage_phonebook():
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", ('Ivan',))
        print("Іздеу нәтижесі:", cur.fetchall())

    
        cur.execute("CALL upsert_contact(%s, %s)", ('Temirlan', '87071234567'))
        
       
        names = ['Asel', 'Berik', 'InvalidUser']
        phones = ['87010001122', '87020003344', '123'] 
        cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))

        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Қате орын алды: {e}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    manage_phonebook()