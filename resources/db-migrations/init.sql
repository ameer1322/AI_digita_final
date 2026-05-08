DROP DATABASE IF EXISTS main;

CREATE DATABASE main;

USE main;

DROP TABLE IF EXISTS order_product;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

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
("Desk lamp", 30, 80),
("Notebook", 8, 500),
("Pen set", 5, 400),
("Coffee mug", 10, 250),
("Phone case", 15, 180)