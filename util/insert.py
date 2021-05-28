import sqlite3
conn = sqlite3.connect('cripto.db', check_same_thread= False)
cur =conn.cursor()

def insert(table_name, columns, values):
    cur.execute('insert into {} ({}) values ("{}")'.format(table_name, columns, values))
    conn.commit()

table_name = "moedas"
columns = "moeda"
values = "btc"

with open('insert.txt', 'r') as file:
   values =  file.readlines()

for i in values:
    j=i.strip()
    print(j)
    insert(table_name, columns, j)

conn.close()