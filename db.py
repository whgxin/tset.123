import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

#conn.execute('CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, name NVARCHAR(20), account NVARCHAR(40), password NVARCHAR(40))')
#print ("Table created successfully")

conn.execute('CREATE TABLE Pictures (id INTEGER PRIMARY KEY AUTOINCREMENT, p_name NVARCHAR(20), p_order INTEGER)')
print ("Table created successfully")

conn.close()