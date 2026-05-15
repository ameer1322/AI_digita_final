DROP DATABASE IF EXISTS main;

CREATE DATABASE main;

USE main;

DROP TABLE IF EXISTS order_product;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS favorites;

CREATE TABLE users(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    join_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products(
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    inventory INT NOT NULL
);

CREATE TABLE favorites(
    product_id INT NOT NULL,
    user_id INT NOT NULL,

    PRIMARY KEY(product_id,user_id),

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE orders(
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    order_shipping_address VARCHAR(255) NOT NULL,
    order_status enum ("TEMP","CLOSED") DEFAULT "TEMP",
    FOREIGN KEY (user_id) REFERENCES users(user_id) on DELETE CASCADE
);

CREATE TABLE order_product(
    order_id INT NOT NULL,
    product_id INT NOT NULL ,
    quantity INT NOT NULL,

    PRIMARY KEY (order_id, product_id),

    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO products (name, price, inventory)
VALUES
("Hunting knife", 30, 70),
("Graphics card", 1200, 7),
("Desktop computer", 2400, 5),
("Kitchen knife", 20, 150),
("T-shirt", 15, 160),
("Hat", 10, 86),
("Sun screen", 5, 200),
("Running shoes", 80, 45),
("Backpack", 55, 60),
("Water bottle", 12, 300),
("Laptop", 999, 15),
("Mouse", 25, 120),
("Keyboard", 45, 90),
("Monitor", 350, 20),
("Headphones", 75, 55),
("Notebook", 8, 500),
("Pen set", 5, 400),
("Coffee mug", 10, 250),
("Phone case", 15, 180),
('Wireless Mouse', 29.99, 100),
('Mechanical Keyboard', 89.99, 50),
('USB Hub', 19.99, 200),
('Monitor Stand', 49.99, 75),
('Webcam HD', 69.99, 60),
('Desk Lamp', 34.99, 90),
('Laptop Sleeve', 24.99, 120),
('Phone Charger', 14.99, 300);


-- DATA FROM CLAUDE FOR MODEL TO TRAIN ON


INSERT INTO users (first_name, last_name, age, email, phone, address, username, hashed_password) VALUES
('Alex',  'Turner',   25, 'alex@email.com',   '0511234567', '10 Dizengoff St',    'alexturner',  'hashed1'),
('Yael',  'Shapiro',  33, 'yael@email.com',   '0512234567', '22 Rothschild Blvd', 'yaelshapiro', 'hashed2'),
('Omer',  'Peretz',   29, 'omer@email.com',   '0513234567', '5 Herzl St',         'omerperetz',  'hashed3'),
('Dana',  'Friedman', 41, 'dana@email.com',   '0514234567', '18 Ben Yehuda St',   'danafried',   'hashed4'),
('Rotem', 'Avraham',  23, 'rotem@email.com',  '0515234567', '33 Allenby St',      'rotema',      'hashed5'),
('Itay',  'Goldberg', 37, 'itay@email.com',   '0516234567', '7 King George St',   'itaygold',    'hashed6'),
('Shira', 'Biton',    28, 'shira@email.com',  '0517234567', '14 Bialik St',       'shirabiton',  'hashed7'),
('Noam',  'Dayan',    45, 'noam@email.com',   '0518234567', '9 Weizmann St',      'noamdayan',   'hashed8'),
('Lihi',  'Carmel',   31, 'lihi@email.com',   '0519234567', '27 Ibn Gabirol St',  'lihicarmel',  'hashed9'),
('Eitan', 'Sasson',   38, 'eitan@email.com',  '0520234567', '3 Namir Rd',         'eitanss',     'hashed10');

-- ORDERS
INSERT INTO orders (user_id, order_shipping_address, order_status) VALUES
-- Alex (6 orders)
(1, '10 Dizengoff St', 'CLOSED'), (1, '10 Dizengoff St', 'CLOSED'), (1, '10 Dizengoff St', 'CLOSED'),
(1, '10 Dizengoff St', 'CLOSED'), (1, '10 Dizengoff St', 'CLOSED'), (1, '10 Dizengoff St', 'CLOSED'),
-- Yael (7 orders)
(2, '22 Rothschild Blvd', 'CLOSED'), (2, '22 Rothschild Blvd', 'CLOSED'), (2, '22 Rothschild Blvd', 'CLOSED'),
(2, '22 Rothschild Blvd', 'CLOSED'), (2, '22 Rothschild Blvd', 'CLOSED'), (2, '22 Rothschild Blvd', 'CLOSED'),
(2, '22 Rothschild Blvd', 'CLOSED'),
-- Omer (6 orders)
(3, '5 Herzl St', 'CLOSED'), (3, '5 Herzl St', 'CLOSED'), (3, '5 Herzl St', 'CLOSED'),
(3, '5 Herzl St', 'CLOSED'), (3, '5 Herzl St', 'CLOSED'), (3, '5 Herzl St', 'CLOSED'),
-- Dana (8 orders)
(4, '18 Ben Yehuda St', 'CLOSED'), (4, '18 Ben Yehuda St', 'CLOSED'), (4, '18 Ben Yehuda St', 'CLOSED'),
(4, '18 Ben Yehuda St', 'CLOSED'), (4, '18 Ben Yehuda St', 'CLOSED'), (4, '18 Ben Yehuda St', 'CLOSED'),
(4, '18 Ben Yehuda St', 'CLOSED'), (4, '18 Ben Yehuda St', 'CLOSED'),
-- Rotem (6 orders)
(5, '33 Allenby St', 'CLOSED'), (5, '33 Allenby St', 'CLOSED'), (5, '33 Allenby St', 'CLOSED'),
(5, '33 Allenby St', 'CLOSED'), (5, '33 Allenby St', 'CLOSED'), (5, '33 Allenby St', 'CLOSED'),
-- Itay (7 orders)
(6, '7 King George St', 'CLOSED'), (6, '7 King George St', 'CLOSED'), (6, '7 King George St', 'CLOSED'),
(6, '7 King George St', 'CLOSED'), (6, '7 King George St', 'CLOSED'), (6, '7 King George St', 'CLOSED'),
(6, '7 King George St', 'CLOSED'),
-- Shira (6 orders)
(7, '14 Bialik St', 'CLOSED'), (7, '14 Bialik St', 'CLOSED'), (7, '14 Bialik St', 'CLOSED'),
(7, '14 Bialik St', 'CLOSED'), (7, '14 Bialik St', 'CLOSED'), (7, '14 Bialik St', 'CLOSED'),
-- Noam (7 orders)
(8, '9 Weizmann St', 'CLOSED'), (8, '9 Weizmann St', 'CLOSED'), (8, '9 Weizmann St', 'CLOSED'),
(8, '9 Weizmann St', 'CLOSED'), (8, '9 Weizmann St', 'CLOSED'), (8, '9 Weizmann St', 'CLOSED'),
(8, '9 Weizmann St', 'CLOSED'),
-- Lihi (6 orders)
(9, '27 Ibn Gabirol St', 'CLOSED'), (9, '27 Ibn Gabirol St', 'CLOSED'), (9, '27 Ibn Gabirol St', 'CLOSED'),
(9, '27 Ibn Gabirol St', 'CLOSED'), (9, '27 Ibn Gabirol St', 'CLOSED'), (9, '27 Ibn Gabirol St', 'CLOSED'),
-- Eitan (7 orders)
(10, '3 Namir Rd', 'CLOSED'), (10, '3 Namir Rd', 'CLOSED'), (10, '3 Namir Rd', 'CLOSED'),
(10, '3 Namir Rd', 'CLOSED'), (10, '3 Namir Rd', 'CLOSED'), (10, '3 Namir Rd', 'CLOSED'),
(10, '3 Namir Rd', 'CLOSED');

-- ORDER PRODUCTS
INSERT INTO order_product (order_id, product_id, quantity) VALUES
-- Alex's orders (1-6) - tech focused, high spender
(1,  11, 1), (1,  12, 1),
(2,  13, 1), (2,  14, 1),
(3,  11, 1), (3,  15, 1),
(4,  12, 2), (4,  20, 1),
(5,  14, 1), (5,  21, 1),
(6,  11, 1), (6,  16, 1),
-- Yael's orders (7-13) - lifestyle/accessories
(7,  5,  2), (7,  6,  1),
(8,  8,  1), (8,  9,  1),
(9,  10, 2), (9,  18, 1),
(10, 5,  1), (10, 19, 2),
(11, 6,  2), (11, 7,  3),
(12, 8,  1), (12, 10, 1),
(13, 9,  1), (13, 18, 2),
-- Omer's orders (14-19) - mixed, medium spender
(14, 2,  1), (14, 12, 1),
(15, 16, 3), (15, 17, 2),
(16, 15, 1), (16, 9,  1),
(17, 13, 1), (17, 16, 1),
(18, 20, 1), (18, 23, 1),
(19, 10, 2), (19, 19, 1),
-- Dana's orders (20-27) - office/tech, high spender
(20, 3,  1), (20, 14, 1),
(21, 2,  1), (21, 13, 1),
(22, 11, 1), (22, 22, 1),
(23, 14, 1), (23, 24, 1),
(24, 21, 1), (24, 16, 2),
(25, 12, 2), (25, 23, 1),
(26, 3,  1), (26, 15, 1),
(27, 11, 1), (27, 20, 1),
-- Rotem's orders (28-33) - budget/everyday items
(28, 7,  4), (28, 17, 3),
(29, 16, 2), (29, 18, 2),
(30, 5,  2), (30, 6,  1),
(31, 10, 3), (31, 19, 1),
(32, 7,  3), (32, 17, 4),
(33, 9,  1), (33, 16, 2),
-- Itay's orders (34-40) - mixed tech and lifestyle
(34, 15, 1), (34, 8,  1),
(35, 20, 1), (35, 13, 1),
(36, 16, 1), (36, 10, 2),
(37, 14, 1), (37, 22, 1),
(38, 12, 1), (38, 9,  1),
(39, 24, 1), (39, 15, 1),
(40, 21, 1), (40, 8,  1),
-- Shira's orders (41-46) - accessories focused
(41, 19, 2), (41, 18, 1),
(42, 25, 1), (42, 6,  2),
(43, 26, 1), (43, 7,  2),
(44, 27, 2), (44, 17, 3),
(45, 10, 2), (45, 16, 1),
(46, 19, 1), (46, 18, 2),
-- Noam's orders (47-53) - high end tech
(47, 3,  1), (47, 2,  1),
(48, 11, 1), (48, 14, 1),
(49, 21, 1), (49, 24, 1),
(50, 2,  1), (50, 15, 1),
(51, 23, 1), (51, 22, 1),
(52, 11, 1), (52, 13, 1),
(53, 14, 1), (53, 20, 1),
-- Lihi's orders (54-59) - everyday + some tech
(54, 8,  1), (54, 9,  1),
(55, 12, 1), (55, 16, 1),
(56, 5,  2), (56, 7,  2),
(57, 22, 1), (57, 10, 2),
(58, 26, 1), (58, 18, 1),
(59, 13, 1), (59, 19, 2),
-- Eitan's orders (60-66) - mixed, medium-high spender
(60, 11, 1), (60, 12, 1),
(61, 8,  1), (61, 15, 1),
(62, 14, 1), (62, 16, 1),
(63, 2,  1), (63, 21, 1),
(64, 9,  1), (64, 22, 1),
(65, 20, 1), (65, 23, 1),
(66, 11, 1), (66, 24, 1);