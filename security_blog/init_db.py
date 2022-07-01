import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('guest', 'guest')
            )

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('admin', '12345678')
            )

connection.commit()
connection.close()