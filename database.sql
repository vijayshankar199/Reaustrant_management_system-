create database restaurant_db;
use restaurant_db;
CREATE TABLE admin(
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50)
);

CREATE TABLE menu(
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    category VARCHAR(50),
    price FLOAT
);

CREATE TABLE orders(
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    mobile_no VARCHAR(20),
    total_amt FLOAT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items(
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    price FLOAT,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(item_id) REFERENCES menu(item_id)
);
