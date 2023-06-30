import sqlite3

conn = sqlite3.connect('database2.db')
print ("Opened database2 successfully")

conn.execute('CREATE TABLE Users2 (id INTEGER PRIMARY KEY AUTOINCREMENT, number NVARCHAR(20), date NVARCHAR(20), hours NVARCHAR(40), money NVARCHAR(40), note NVARCHAR(40))')
print ("Table created successfully")
conn.close()