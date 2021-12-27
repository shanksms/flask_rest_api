import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "create table user (id int, username text, password text)"
insert_query = "insert into user values (?, ?, ?)"
cursor.execute(create_table)
users = [
    (1, 'jose', 'asdf'),
    (2, 'rolf', 'asdf'),
    (1, 'anne', 'asdf')
]
cursor.executemany(insert_query, users)
connection.commit()
connection.close()
