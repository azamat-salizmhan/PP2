import psycopg2
import csv
from connect import get_connection

def import_csv(file_name):
    conn = get_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        with open(file_name, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute(
                    "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s) ON CONFLICT (phone_number) DO NOTHING",
                    (row['first_name'], row['last_name'], row['phone_number'])
                )
        conn.commit()
        print(f"Successfully imported data from {file_name}")
    except Exception as e:
        print(f"CSV Error: {e}")
    finally:
        conn.close()

def add_contact_console():
    fname = input("Enter First Name: ")
    lname = input("Enter Last Name: ")
    phone = input("Enter Phone Number: ")
    
    conn = get_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
            (fname, lname, phone)
        )
        conn.commit() 
        print("Contact added successfully!")
    except Exception as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

def update_contact():
    name = input("Enter the First Name of the contact to update: ")
    new_phone = input("Enter the new Phone Number: ")
    
    conn = get_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contacts SET phone_number = %s WHERE first_name = %s",
            (new_phone, name)
        )
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Successfully updated {name}'s phone number.")
        else:
            print("Contact not found.")
    except Exception as e:
        print(f"Update Error: {e}")
    finally:
        conn.close()

def query_contacts():
    search_term = input("Enter a name or phone number to search: ")
    
    conn = get_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM contacts WHERE first_name ILIKE %s OR phone_number LIKE %s"
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        
        results = cursor.fetchall()
        if results:
            print("\n--- Search Results ---")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Phone: {row[3]}")
        else:
            print("No matching contacts found.")
    except Exception as e:
        print(f"Query Error: {e}")
    finally:
        conn.close()

def delete_contact():
    name = input("Enter the First Name of the contact to delete: ")
    
    conn = get_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE first_name = %s", (name,))
        conn.commit()
        print(f"Contact {name} deleted (if they existed).")
    except Exception as e:
        print(f"Delete Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Import CSV")
        print("2. Add Contact manually")
        print("3. Update Contact")
        print("4. Search/Query Contacts")
        print("5. Delete Contact")
        print("6. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            import_csv('contacts.csv')
        elif choice == '2':
            add_contact_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")