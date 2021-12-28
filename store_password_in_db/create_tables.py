import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user_table = "create table user (id integer Primary key, username text, password text)"
cursor.execute(create_user_table)
create_item_table = "create table item (id integer Primary key, name text, price float)"
cursor.execute(create_item_table)
connection.commit()
connection.close()
