import psycopg2
import psycopg2.extras as pe

DB_HOST = '127.0.0.1'
DB_USER = 'postgres'
DB_NAME = 'postgres'
DB_PASS = 'this will be the password'


connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

curs = connection.cursor(cursor_factory=pe.DictCursor)

# queries will go here as curs.execute("")

connection.commit()

curs.close()

connection.close()
# with connection:
#     curs = connection.cursor(cursor_factory=pe.DictCursor)
#     with curs:
#         curs.execute("")
