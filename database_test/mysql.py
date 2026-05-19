import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='SHS',
)


def insert_user():
    name = input('Enter your name: ')
    age = int(input('Enter your age: '))
    email = input('Enter your email address: ')

    insert_query ="""INSERT INTO students(name, age, email) values (%s, %s, %s)"""

    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_query, (name, age, email))
            conn.commit()

    except Exception as x:
         print(x)


insert_user()

try:
    with conn.cursor() as cursor:
        cursor.execute('SElECT * FROM Students')

        result = cursor.fetchall()

        for row in result:
            print(row)
finally:
    conn.close()