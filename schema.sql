-- schema.sql
-- Crestview Campus Bookstore: orders, textbooks, and changes waiting for staff.

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    student TEXT NOT NULL,
    title     TEXT NOT NULL,
    status   TEXT NOT NULL,
    pickup_desk  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS textbooks (
    name  TEXT PRIMARY KEY,
    course TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS change_requests (
    number      INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    TEXT NOT NULL,
    new_pickup_desk TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'waiting'
);

INSERT OR IGNORE INTO orders (order_id, student, title, status, pickup_desk) VALUES
    ('B400', 'Mia Park', 'Intro to Accounting', 'ready for pickup', 'North Desk'),
    ('B401', 'Chris Lee', 'Principles of Finance', 'ordered', 'North Desk'),
    ('B402', 'Mike Brown', 'Principles of Managerial Accounting', 'picked up', 'South Desk'),
    ('B403', 'Mark Smith', 'Principles of Microeconomics', 'cancelled', 'North Desk'),
    ('B404', 'Leo Grant', 'Business Statistics', 'ordered', 'South Desk');

INSERT OR IGNORE INTO textbooks (name, course, price, stock) VALUES
    ('Intro to Accounting', 'ACG2021', 120.00, 4),
    ('Principles of Finance', 'FIN3403', 99.00, 2),
    ('Principles of Managerial Accounting', 'ACG2071', 160.00, 15),
    ('Principles of Microeconomics', 'ECO2023', 111.00, 1),
    ('Business Statistics', 'QMB3200', 95.00, 0);