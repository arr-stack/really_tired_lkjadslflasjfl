import sqlite3


con = sqlite3.connect('events.db')
con.execute("PRAGMA foreign_keys = ON;")
cur = con.cursor()
cur.execute('CREATE TABLE events(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date DATE, description TEXT, people_amount INTEGER NOT NULL, '
            'people_max INTEGER NOT NULL, time_start TIME NOT NULL, time_end TIME NOT NULL)')
cur.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, name TEXT, password TEXT)')
cur.execute("""CREATE TABLE registrations(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                event_id INTEGER,
                user_id INTEGER, 
                time_slot_start TIME NOT NULL, 
                time_slot_end TIME NOT NULL, 
                FOREIGN KEY(user_id) REFERENCES users(id), 
                FOREIGN KEY(event_id) REFERENCES events(id))""")

users_data = [
    ("alice@example.com", "alice", "hashed_password_123"),
    ("bob@example.com", "bob", "hashed_password_456"),
    ("charlie@example.com", "charlie", "hashed_password_789"),
]

cur.executemany(
    "INSERT INTO users (email, name, password) VALUES (?, ?, ?)", users_data
)

events_data = [
    (
        "Python Workshop",
        "2026-06-15",
        "Learn the basics of Python and SQLite.",
        10,
        30,
        "10:00:00",
        "13:00:00",
    ),
    (
        "AI Hackathon",
        "2026-07-20",
        "Build cool AI projects in 24 hours.",
        5,
        50,
        "09:00:00",
        "18:00:00",
    ),
]

cur.executemany(
    """INSERT INTO events 
       (title, date, description, people_amount, people_max, time_start, time_end) 
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    events_data,
)


registrations_data = [
    (1, 1, "10:00:00", "11:30:00"),
    (1, 2, "10:30:00", "12:00:00"),
    (2, 1, "09:00:00", "12:00:00"),
]

cur.executemany(
    """INSERT INTO registrations 
       (event_id, user_id, time_slot_start, time_slot_end) 
       VALUES (?, ?, ?, ?)""",
    registrations_data,
)

con.commit()
con.close()