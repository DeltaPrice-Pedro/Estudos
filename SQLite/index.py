import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_NAME = 'sesas_db.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE = 'sesas_users'

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute(
    f'CREATE TABLE IF NOT EXISTS {TABLE}'
    '('
    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    'nome VARCHAR(100),'
    'idade INTEGER'
    ')'
)
connection.commit()

cursor.execute(
    f'DELETE FROM sqlite_sequence WHERE name="{TABLE}"'
)
connection.commit()

sql = (
    f'INSERT INTO {TABLE} '
    '(name, weight) '
    'VALUES '
    '(:nome, :peso)'
)
cursor.executemany(sql, (
    {'nome': 'Joãozinho', 'peso': 3},
    {'nome': 'Maria', 'peso': 2},
))


cursor.execute(
    f'SELECT * FROM {TABLE} '
    'WHERE id = "3"'
)
for row in cursor.fetchall():
    _id, name, weight = row
    print(_id, name, weight)

cursor.close()
connection.close()

