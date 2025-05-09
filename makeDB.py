import sqlite3

# Создаем базу данных
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()

# Создаем таблицу рейсов
cursor.execute('''
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY,
    departure_city TEXT,
    arrival_city TEXT,
    departure_time TEXT,
    arrival_time TEXT,
    flight_duration INTEGER
)
''')

# Вставляем тестовые данные
cursor.executemany('''
INSERT INTO flights (departure_city, arrival_city, departure_time, arrival_time, flight_duration)
VALUES (?, ?, ?, ?, ?)
''', [
    ('Пермь', 'Москва', '2025-05-10 08:00', '2025-05-10 10:00', 120),
    ('Москва', 'Дубай', '2025-05-10 12:00', '2025-05-10 18:00', 240),
    ('Пермь', 'Москва', '2025-05-10 09:00', '2025-05-10 11:00', 120),
    ('Москва', 'Дубай', '2025-05-10 13:00', '2025-05-10 19:00', 240),
    ('Пермь', 'Москва', '2025-05-10 07:00', '2025-05-10 09:00', 120),
    ('Москва', 'Дубай', '2025-05-10 14:00', '2025-05-10 20:00', 240)
])

# Сохраняем и закрываем соединение
conn.commit()
conn.close()
