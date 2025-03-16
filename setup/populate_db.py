import sqlite3
import json

# Load JSON data
with open('setup/geographical_data.json', 'r') as f:
    data = json.load(f)

# Connect to SQLite database
conn = sqlite3.connect('geographical_data.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL
)
''')

cursor.execute('''
CREATE TABLE distances (
    from_city_id INTEGER,
    to_city_id INTEGER,
    distance_km REAL,
    FOREIGN KEY (from_city_id) REFERENCES cities (id),
    FOREIGN KEY (to_city_id) REFERENCES cities (id)
)
''')

cursor.execute('''
CREATE TABLE transportation (
    from_city_id INTEGER,
    to_city_id INTEGER,
    mode TEXT,
    duration_hours REAL,
    FOREIGN KEY (from_city_id) REFERENCES cities (id),
    FOREIGN KEY (to_city_id) REFERENCES cities (id)
)
''')

cursor.execute('''
CREATE TABLE weather (
    city_id INTEGER,
    date TEXT,
    condition TEXT,
    temperature_c REAL,
    FOREIGN KEY (city_id) REFERENCES cities (id)
)
''')

# Insert data into tables
for city in data['cities']:
    cursor.execute('INSERT INTO cities VALUES (?, ?, ?, ?, ?)',
                   (city['id'], city['name'], city['country'], city['latitude'], city['longitude']))

for distance in data['distances']:
    cursor.execute('INSERT INTO distances VALUES (?, ?, ?)',
                   (distance['from_city_id'], distance['to_city_id'], distance['distance_km']))

for transport in data['transportation']:
    cursor.execute('INSERT INTO transportation VALUES (?, ?, ?, ?)',
                   (transport['from_city_id'], transport['to_city_id'], transport['mode'], transport['duration_hours']))

for weather in data['weather']:
    cursor.execute('INSERT INTO weather VALUES (?, ?, ?, ?)',
                   (weather['city_id'], weather['date'], weather['condition'], weather['temperature_c']))

# Commit and close
conn.commit()
conn.close()

print("Data successfully inserted into SQLite database!")