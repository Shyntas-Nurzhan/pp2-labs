import psycopg2
import csv
from config import load_config
from psycopg2 import sql

def create_table():
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebooknew (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(filename='insertnew.csv'):
    import ast
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    data = []

    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    data.append(row)

        # Преобразуем данные в pg-массив
        pg_array = '{{{}}}'.format(','.join(['"{{{0},{1}}}"'.format(r[0], r[1]) for r in data]))
        cur.execute("CALL insert_many_users(%s::text[][]);", (pg_array,))
        conn.commit()
        print("Batch insert completed.")
    except Exception as e:
        print("CSV insert error:", e)
    finally:
        cur.close()
        conn.close()

def update_user():
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")
    cur.execute("CALL insert_or_update_user(%s, %s);", (name, new_phone))
    conn.commit()
    cur.close()
    conn.close()

def query_data():
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    choice = input("Enter search pattern (or press Enter to show all): ")
    if choice.strip() == "":
        cur.execute("SELECT * FROM phonebooknew ORDER BY id;")
    else:
        cur.execute("SELECT * FROM search_phonebook(%s);", (choice,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def query_with_pagination():
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    cur.execute("SELECT * FROM get_paginated_records(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_entry():
    conn = psycopg2.connect(**load_config())
    cur = conn.cursor()
    value = input("Enter username or phone to delete: ")
    cur.execute("CALL delete_user(%s);", (value,))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    while True:
        print("\n1. Insert from console\n2. Insert from CSV\n3. Update\n4. Query\n5. Delete\n6. Exit\n7. Query with pagination")
        opt = input("Choose option: ")
        if opt == '1':
            insert_from_console()
        elif opt == '2':
            insert_from_csv()
        elif opt == '3':
            update_user()
        elif opt == '4':
            query_data()
        elif opt == '5':
            delete_entry()
        elif opt == '6':
            break
        elif opt == '7':
            query_with_pagination()
        else:
            print("Invalid option.")
