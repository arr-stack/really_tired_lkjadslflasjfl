import sqlite3

con = sqlite3.connect('events.db')
cur = con.cursor()
cur.execute('CREATE TABLE events(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date DATETIME, description TEXT, people_amount INTEGER NOT NULL, people_max INTEGER NOT NULL)')
cur.execute('CREATE TABLE registrations(id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER FOREIGN KEY, user_id INTEGER FOREIGN KEY)')
cur.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, name TEXT, password TEXT)')
con.commit()
con.close()