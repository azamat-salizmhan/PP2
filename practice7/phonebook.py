
import csv
from connect import get_connection, create_table



def insert_from_csv(filepath: str):
    
    conn = get_connection()
    inserted = 0
    skipped = 0
    try:
        with conn:
            with conn.cursor() as cur, open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    firstname = row.get("firstname", "").strip()
                    lastname  = row.get("lastname",  "").strip()
                    phone     = row.get("phone",     "").strip()
                    if not firstname or not phone:
                        skipped += 1
                        continue
                    try:
                        cur.execute(
                            """INSERT INTO phonebook (firstname, lastname, phone)
                               VALUES (%s, %s, %s)
                               ON CONFLICT (phone) DO NOTHING""",
                            (firstname, lastname or None, phone)
                        )
                        if cur.rowcount:
                            inserted += 1
                        else:
                            skipped += 1
                    except Exception as e:
                        print(f"  [WARN] Skipping row {row}: {e}")
                        skipped += 1
        print(f"[CSV] Inserted {inserted} rows, skipped {skipped}.")
    finally:
        conn.close()


def insert_from_console():
    
    firstname = input("First name: ").strip()
    lastname  = input("Last name (leave blank if none): ").strip()
    phone     = input("Phone: ").strip()

    if not firstname or not phone:
        print("[ERROR] First name and phone are required.")
        return

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO phonebook (firstname, lastname, phone)
                       VALUES (%s, %s, %s)
                       ON CONFLICT (phone) DO NOTHING""",
                    (firstname, lastname or None, phone)
                )
                if cur.rowcount:
                    print("[OK] Contact added.")
                else:
                    print("[INFO] Phone already exists – nothing inserted.")
    finally:
        conn.close()



def _print_rows(rows):
    if not rows:
        print("  (no results)")
        return
    print(f"  {'ID':<5} {'First name':<15} {'Last name':<15} {'Phone':<20}")
    print("  " + "-" * 57)
    for r in rows:
        print(f"  {r[0]:<5} {r[1]:<15} {(r[2] or ''):<15} {r[3]:<20}")


def search_all():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, firstname, lastname, phone FROM phonebook ORDER BY firstname")
            _print_rows(cur.fetchall())
    finally:
        conn.close()


def search_by_name(name: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, firstname, lastname, phone FROM phonebook
                   WHERE firstname ILIKE %s OR lastname ILIKE %s
                   ORDER BY firstname""",
                (f"%{name}%", f"%{name}%")
            )
            _print_rows(cur.fetchall())
    finally:
        conn.close()


def search_by_phone_prefix(prefix: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, firstname, lastname, phone FROM phonebook
                   WHERE phone LIKE %s
                   ORDER BY phone""",
                (f"{prefix}%",)
            )
            _print_rows(cur.fetchall())
    finally:
        conn.close()



def update_by_phone():
    
    phone = input("Enter the phone number of the contact to update: ").strip()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, firstname, lastname, phone FROM phonebook WHERE phone = %s",
                (phone,)
            )
            row = cur.fetchone()
        if not row:
            print("[INFO] No contact found with that phone.")
            return
        print(f"  Found: {row[1]} {row[2] or ''}, {row[3]}")

        print("What do you want to update?")
        print("  1. First name")
        print("  2. Last name")
        print("  3. Phone")
        choice = input("Choice (1/2/3): ").strip()

        if choice == "1":
            new_val = input("New first name: ").strip()
            field = "firstname"
        elif choice == "2":
            new_val = input("New last name: ").strip()
            field = "lastname"
        elif choice == "3":
            new_val = input("New phone: ").strip()
            field = "phone"
        else:
            print("[ERROR] Invalid choice.")
            return

        if not new_val:
            print("[ERROR] Value cannot be empty.")
            return

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE phonebook SET {field} = %s WHERE phone = %s",
                    (new_val, phone)
                )
        print("[OK] Contact updated.")
    finally:
        conn.close()



def delete_contact():
    print("Delete by:")
    print("  1. Username (first name)")
    print("  2. Phone")
    choice = input("Choice (1/2): ").strip()

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                if choice == "1":
                    name = input("First name to delete: ").strip()
                    cur.execute("DELETE FROM phonebook WHERE firstname ILIKE %s", (name,))
                elif choice == "2":
                    phone = input("Phone to delete: ").strip()
                    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
                else:
                    print("[ERROR] Invalid choice.")
                    return
                print(f"[OK] Deleted {cur.rowcount} row(s).")
    finally:
        conn.close()



def menu():
    create_table()
    while True:
        print("\n═══════════ PhoneBook ═══════════")
        print(" 1. Import contacts from CSV")
        print(" 2. Add contact (console)")
        print(" 3. Show all contacts")
        print(" 4. Search by name")
        print(" 5. Search by phone prefix")
        print(" 6. Update a contact")
        print(" 7. Delete a contact")
        print(" 0. Exit")
        print("═════════════════════════════════")
        choice = input("Choose: ").strip()

        if choice == "1":
            path = input("CSV file path [contacts.csv]: ").strip() or "contacts.csv"
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            search_all()
        elif choice == "4":
            name = input("Name to search: ").strip()
            search_by_name(name)
        elif choice == "5":
            prefix = input("Phone prefix: ").strip()
            search_by_phone_prefix(prefix)
        elif choice == "6":
            update_by_phone()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("[ERROR] Unknown option.")


if __name__ == "__main__":
    menu()