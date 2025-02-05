import psycopg2
import configparser

config = configparser.ConfigParser()
config.read("settings_ignore.ini")
db_name = config['Database']['db_name']
db_user = config['Database']['db_user']
db_password = config['Database']['db_password']

# https://www.psycopg.org/docs/usage.html

conn = None

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE ClientPhone;
        DROP TABLE client;
        DROP TABLE phone;
        """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS client (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(20) NOT NULL,
                    last_name VARCHAR(20) NOT NULL,
                    email VARCHAR(50) NOT NULL
                );
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS phone (
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(20)
                );
                """)
        conn.commit()

        cur.execute("""
                CREATE TABLE IF NOT EXISTS ClientPhone (
                    client_id INTEGER REFERENCES client(id),
                    phone_id INTEGER REFERENCES phone(id),
                    CONSTRAINT pk PRIMARY KEY (client_id, phone_id)
                );
                """)
        conn.commit()

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:

        cur.execute("""
                INSERT INTO client (first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
                """, (first_name, last_name, email))

        client_id = cur.fetchone()[0]
        print(f"Клиент {client_id} добавлен в базу")

        if phone is not None:
            cur.execute("""
                    INSERT INTO phone (phone) VALUES(%s) RETURNING id;
                    """, (phone, ))

            phone_id = cur.fetchone()[0]
            print(f"Телефон {phone} добавлен в базу")

            cur.execute("""
                    INSERT INTO ClientPhone (client_id, phone_id) VALUES(%s, %s);
                    """, (client_id, phone_id))
            print(f"IDs: {client_id}, {phone_id} добавлены в базу")
            conn.commit()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO phone (phone) VALUES(%s) RETURNING id;
                """, (phone,))

        phone_id = cur.fetchone()[0]
        print(f"Телефон {phone} добавлен в базу")

        cur.execute("""
                INSERT INTO ClientPhone (client_id, phone_id) VALUES(%s, %s);
                """, (client_id, phone_id))
        print(f"IDs {client_id}, {phone_id} добавлены в базу")
        conn.commit()
        print(f"Телефон {phone} для пользователя {client_id} добавлен в базу")

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:

        cur.execute("""
                UPDATE client SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
                """, (first_name, last_name, email, client_id))

        if phone is not None:
            cur.execute("""
                    INSERT INTO phone (phone) VALUES(%s) RETURNING id;
                    """, (phone, ))

            phone_id = cur.fetchone()[0]
            print(f"Телефон {phone} добавлен в базу")

            cur.execute("""
                    INSERT INTO ClientPhone (client_id, phone_id) VALUES(%s, %s);
                    """, (client_id, phone_id))
            print(f"IDs: {client_id}, {phone_id} добавлены в базу")
            conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM ClientPhone WHERE client_id=%s AND phone_id=(SELECT id FROM phone WHERE phone=%s);
                """, (client_id, phone))
        conn.commit()
        cur.execute("""
                DELETE FROM phone WHERE phone=%s RETURNING id;
                """, (phone, ))
        conn.commit()
        print(f"Телефон {phone} для пользователя {client_id} удален из базы")

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM ClientPhone WHERE client_id=%s RETURNING phone_id;
                """, (client_id, ))
        phone_id = cur.fetchall()
        print(phone_id)
        for phone in phone_id:
            cur.execute("""
                    DELETE FROM phone WHERE id=%s;
                    """, phone)
            conn.commit()
        print(f"Пользователь {client_id} удален из базы")

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                SELECT * FROM client c, phone JOIN clientphone cp ON c.id=cp.client_id JOIN phone p ON p.id=cp.phone_id WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR phone LIKE %s;
                """, (first_name, last_name, email, phone))
        print(cur.fetchall())

# SELECT *
# FROM client c
# JOIN clientphone cp ON c.id=cp.client_id
# JOIN phone p ON p.id=cp.phone_id
# WHERE first_name LIKE '' OR last_name LIKE '' OR email LIKE '' OR phone LIKE '';

with psycopg2.connect(database=db_name, user=db_user, password=db_password) as conn:
    create_db(conn)

    if __name__ == '__main__':
        add_client(conn, "Michael", "Jackson", "michael@jackson.com", "+78885558811")
        add_client(conn, "Xpen", "From_mountain", "xren@sbugra.com")
        add_client(conn, "Мао", "Дзедун", "unclemao@ali.com")
        add_phone(conn, 2, "+13217778833")
        change_client(conn, 3, "Мао", "Дзедун", "unclemao@ali.com", "+43336663399")
        add_phone(conn, 3, "+99992226633")
        # delete_phone(conn, 3, "+99992226633")
        # delete_client(conn, 3)
        find_client(conn, first_name="Мао")