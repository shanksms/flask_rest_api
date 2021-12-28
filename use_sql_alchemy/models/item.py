import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def get_item_by_name(cls, name):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            sql = '''
                              select name, price from item where name=?
                       '''
            result = cursor.execute(sql, (name,))
            row = result.fetchone()
        finally:
            connection.close()
        if row:
            return cls(name=row[0], price=row[1])
        else:
            return None

    def insert(self):
        status = 1
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            insert_sql = '''
                     insert into item
                     (name, price)
                     values
                     (?, ?)
                     '''
            result = cursor.execute(insert_sql, (self.name, self.price))
            print(result)
            connection.commit()
        except Exception as exc:
            print('exception occurred', exc)
            status = 0
        finally:
            connection.close()
        return status

    def update(self):
        status = 1
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            update_sql = 'update item set price=? where name=?'
            result = cursor.execute(update_sql, (self.price, self.name))
            connection.commit()
            print(f'{result.rowcount} rows updated')
        except Exception as exc:
            print('exception occurred', exc)
            status = 0
        finally:
            connection.close()
        return status
