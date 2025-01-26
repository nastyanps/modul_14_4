import sqlite3


def initiate_db():
    connection = sqlite3.connect('products_14_4.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    name_photo TEXT
    )
    ''')


def insert_product(pr_id, *args):
    connection = sqlite3.connect('products_14_4.db')
    cursor = connection.cursor()
    check_users = cursor.execute('SELECT * FROM Products WHERE id = ?', (pr_id,))
    if check_users.fetchone() is None:
        cursor.execute('INSERT INTO Products VALUES (?, ?, ?, ?, ?)',
                       (pr_id, *args))
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('products_14_4.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    all_products = cursor.fetchall()
    connection.close()
    return all_products


initiate_db()
products = [
    {'title': 'МИНИмальный курс', 'description': 'Курс - маленький, но удаленький)', 'price': '100 $',
     'name_photo': 'mini.png'},
    {'title': 'БАЗовый курс', 'description': 'Курс - маленький и сладенький)', 'price': '200 $',
     'name_photo': 'basic.png'},
    {'title': 'ОПТИмальный курс', 'description': 'Курс - большой и сладенький)', 'price': '300 $',
     'name_photo': 'opti.png'},
    {'title': 'МАКСИмальный курс', 'description': 'Курс - МЕГА большой и сладенький)', 'price': '400 $',
     'name_photo': 'maxi.png'}
]
for index, product in enumerate(products, start=1):
    insert_product(index, product['title'], product['description'], product['price'], product['name_photo'])
