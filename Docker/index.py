import os
import pymysql
import dotenv

dotenv.load_dotenv()

connection = pymysql.connect(
    host= os.environ['MYSQL_HOST'],
    user= os.environ['MYSQL_USER'],
    password= os.environ['MYSQL_PASSWORD'],
    database= os.environ['MYSQL_DATABASE']
)

with connection:
    with connection.cursor() as cursor:
        cursor.execute(
            'CREATE TABLE users ('
            'id INT NOT NULL AUTO_INCREMENT, '
            'nome VARCHAR(50) NOT NULL, '
            'idade INT, '
            'PRIMARY KEY(id)'
            ') '
        )
        connection.commit()
        print('deu')
