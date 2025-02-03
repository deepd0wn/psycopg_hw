import psycopg2

def create_db(conn):
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE ClientPhone;
            DROP TABLE Client;
            DROP TABLE Phone;
            """)

            cur.execute("""
                    CREATE TABLE IF NOT EXISTS Client(
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL
                        last_name VARCHAR(50) NOT NULL
                        email VARCHAR(50) NOT NULL
                    );
                    """)

            cur.execute("""
                    CREATE TABLE IF NOT EXISTS Phone(
                        id SERIAL PRIMARY KEY,
                        phone VARCHAR(20) NOT NULL,
                    );
                    """)
            conn.commit()

            cur.execute("""
                    CREATE TABLE IF NOT EXISTS ClientPhone(
                        client_id INTEGER REFERENCES Client(id),
	                    phone_id INTEGER REFERENCES Phone(id),
	                    CONSTRAINT pk PRIMARY KEY (client_id, phone_id)
                    );
                    """)
            conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO client(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
                """, (first_name, last_name, email))
        # conn.commit()
        print(cur.fetchone())

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO phone(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))
        conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, first_name, last_name, email, phones=None)
    add_client(conn, first_name, last_name, email, phones=None)
    add_client(conn, first_name, last_name, email, phones=None)
    add_client(conn, first_name, last_name, email, phones=None)
    add_client(conn, first_name, last_name, email, phones=None)
    add_phone(conn, client_id, phone)
    add_phone(conn, client_id, phone)
    add_phone(conn, client_id, phone)
    change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None)
    delete_phone(conn, client_id, phone)
    delete_client(conn, client_id)
    find_client(conn, first_name=None, last_name=None, email=None, phone=None)