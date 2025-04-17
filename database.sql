CREATE DATABASE IF NOT EXISTS employee_db;

USE employee_db;

# user information
CREATE TABLE IF NOT EXISTS employee(
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(15) Null,
    lastName varchar(15) Null,
    userName varchar(15),
    password varchar(25) null,
    role enum('employee','manager','owner')
    );
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','is the best','admin','admin','owner');
# todo get rid of when done for testing purposes only
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','Jaffe','e','e','owner');
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','is thn','m','m','owner');
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','Yes I am the ','o','o','owner');

# employee close
Create Table if not exists employee_close(
    firstName Varchar (15),
    lastName varchar (15),
    store_name VARCHAR(25),
    credit DECIMAL(10, 2),
    cash_in_envelope DECIMAL(10, 2),
    expense DECIMAL(10, 2),
    comments TEXT,
    employee_id INT,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

# table for store
CREATE TABLE if not exists Store (
    store_id INT Auto_Increment primary key,
    store_name VARCHAR(255),
    location VARCHAR(255)
);

# employee clock-in and clock to
Create table if not exists clockTable(
    clock_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    store_id INT,
    clock_in DATETIME,
    clock_out DATETIME,
    reg_in DECIMAL(10,2),
    reg_out DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);


# table for invoices
CREATE TABLE if not exists Invoice (
    invoice_id INT AUTO_INCREMENT primary key,
    company_name VARCHAR(255),
    amount_due DECIMAL(10,2),
    due_date DATE,
    paid_status ENUM('paid', 'unpaid'),
    payment_date DATE
);

# table for bonuses
CREATE TABLE if not exists Bonuses (
    bonus_id INT auto_increment PRIMARY KEY,
    employee_id INT,
    store_id INT,
    week_start DATE,
    week_end DATE,
    total_sales DECIMAL(10,2),
    bonus_percentage DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);


INSERT INTO employee (firstName, lastName, userName, password, role) VALUES
('Dan', 'Jones', 'admin', 'admin', 'owner'),
('John', 'Doe', 'johndoe', 'password123', 'manager'),
('Jane', 'Smith', 'janesmith', 'password456', 'employee'),
('Mike', 'Jones', 'mikejones', 'password789', 'employee');

INSERT INTO employee_close (firstName, lastName, store_name, credit, cash_in_envelope, expense, comments, employee_id) VALUES
('Dan', 'Jones', 'Beach Store', 1000.50, 150.00, 500.00, 'Everything is running smoothly.', 1),
('John', 'Doe', 'City Store', 850.00, 200.00, 300.00, 'Needs more staff.', 2),
('Jane', 'Smith', 'Downtown Store', 900.00, 120.00, 350.00, 'Some items went out of stock.', 3),
('Mike', 'Jones', 'Suburb Store', 950.00, 180.00, 400.00, 'Good sales this week.', 4);

INSERT INTO Store (store_name, location) VALUES
('Beach Store', 'Clearwater Beach'),
('City Store', 'Downtown City Center'),
('Downtown Store', 'Main Street'),
('Suburb Store', 'Greenfield Suburbs');

INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES
(1, 1, '2025-04-16 09:00:00', '2025-04-16 17:00:00', 8.00, 0.00),
(2, 2, '2025-04-16 08:00:00', '2025-04-16 16:00:00', 8.00, 0.00),
(3, 3, '2025-04-16 10:00:00', '2025-04-16 18:00:00', 8.00, 0.00),
(4, 4, '2025-04-16 11:00:00', '2025-04-16 19:00:00', 8.00, 0.00);

INSERT INTO Invoice (company_name, amount_due, due_date, paid_status, payment_date) VALUES
('ABC Corp', 1500.00, '2025-05-01', 'unpaid', NULL),
('XYZ Ltd', 2000.00, '2025-05-15', 'paid', '2025-04-10'),
('Global Tech', 2500.00, '2025-06-01', 'unpaid', NULL),
('QuickShop Inc.', 1200.00, '2025-05-05', 'paid', '2025-04-20');

INSERT INTO Bonuses (employee_id, store_id, week_start, week_end, total_sales, bonus_percentage) VALUES
(1, 1, '2025-04-01', '2025-04-07', 10000.00, 5.00),
(2, 2, '2025-04-01', '2025-04-07', 12000.00, 4.50),
(3, 3, '2025-04-01', '2025-04-07', 11000.00, 5.50),
(4, 4, '2025-04-01', '2025-04-07', 9000.00, 4.00);
