import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "create table user (id integer Primary key, username text, password text)"
cursor.execute(create_table)
connection.commit()
connection.close()
