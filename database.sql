DROP DATABASE IF EXISTS employee_db;
CREATE DATABASE IF NOT EXISTS employee_db;
USE employee_db;

CREATE TABLE IF NOT EXISTS Store (
                                     store_id INT AUTO_INCREMENT PRIMARY KEY,
                                     store_name VARCHAR(255),
                                     location VARCHAR(255) 
);

CREATE TABLE IF NOT EXISTS employee (
                                        employee_id INT AUTO_INCREMENT PRIMARY KEY,
                                        firstName VARCHAR(15) NULL,
                                        lastName VARCHAR(15) NULL,
                                        userName VARCHAR(15),
                                        password VARCHAR(25) NULL,
                                        role ENUM('employee', 'manager', 'owner'),
                                        bonus_percentage DECIMAL(10,2),
                                        hourlyRate DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    expense_type VARCHAR(150),
    expense_date DATE,
    employee_id INT,
    expense_value DECIMAL(10,2),
    store_id INT,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);

CREATE TABLE IF NOT EXISTS merchandise (
                                           merchandise_id INT PRIMARY KEY AUTO_INCREMENT,
                                           merchandise_type VARCHAR(150),
                                           merchandise_date DATE,
                                           store_id INT,
                                           quantity INT,
                                           unitPrice DECIMAL(10, 2),
                                           employee_id INT,
                                           FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
                                           FOREIGN KEY (store_id) REFERENCES Store(store_id)

);

CREATE TABLE IF NOT EXISTS employee_close (
    close_id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(15),
    lastName VARCHAR(15),
    store_name VARCHAR(25),
    credit DECIMAL(10, 2),
    cash_in_envelope DECIMAL(10, 2),
    expense DECIMAL(10, 2),
    comments TEXT,
    employee_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    UNIQUE KEY store_date_unique (store_name, timestamp)
);


CREATE TABLE IF NOT EXISTS clockTable (
                                          clock_id INT AUTO_INCREMENT PRIMARY KEY,
                                          employee_id INT,
                                          store_id INT,
                                          clock_in DATETIME,
                                          clock_out DATETIME,
                                          reg_in DECIMAL(10,2),
                                          reg_out DECIMAL(10,2),
                                          FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
                                          FOREIGN KEY (store_id) REFERENCES Store(store_id)
);

CREATE TABLE IF NOT EXISTS Invoice (
                                       invoice_id INT AUTO_INCREMENT PRIMARY KEY,
                                       company_name VARCHAR(255),
                                       amount DECIMAL(10,2),
                                       due_date DATE,
                                       recieved_date DATE,
                                       paid_status ENUM('paid', 'unpaid'),
                                       payment_date DATE,
                                       store_id INT,
                                       amount_paid DECIMAL(10,2),
                                       FOREIGN KEY (store_id) REFERENCES Store(store_id)
);
CREATE TABLE IF NOT EXISTS Payroll (
                                       payroll_id INT AUTO_INCREMENT PRIMARY KEY,
                                       date DATE,
                                       bonuses DECIMAL(10,2),
                                       wages DECIMAL(10,2),
                                       store_id INT,
                                       FOREIGN KEY (store_id) REFERENCES Store(store_id)
);

DELIMITER //

CREATE TRIGGER before_employee_insert 
BEFORE INSERT ON employee
FOR EACH ROW
BEGIN
    IF NEW.bonus_percentage < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bonus percentage cannot be negative';
    END IF;
END//

CREATE TRIGGER before_employee_update
BEFORE UPDATE ON employee
FOR EACH ROW
BEGIN
    IF NEW.bonus_percentage < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bonus percentage cannot be negative';
    END IF;
END//

CREATE TRIGGER before_payroll_insert 
BEFORE INSERT ON Payroll
FOR EACH ROW
BEGIN
    IF NEW.bonuses < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bonuses cannot be negative';
    END IF;
END//

CREATE TRIGGER before_payroll_update
BEFORE UPDATE ON Payroll
FOR EACH ROW
BEGIN
    IF NEW.bonuses < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bonuses cannot be negative';
    END IF;
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_invoice_insert 
BEFORE INSERT ON Invoice
FOR EACH ROW
BEGIN
    IF NEW.amount_paid > NEW.amount THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Amount paid cannot be greater than total amount';
    END IF;
END//

CREATE TRIGGER before_invoice_update
BEFORE UPDATE ON Invoice
FOR EACH ROW
BEGIN
    IF NEW.amount_paid > NEW.amount THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Amount paid cannot be greater than total amount';
    END IF;
END//

DELIMITER ;


-- Insert Data

-- Insert 3 stores
INSERT INTO Store (store_name, location)
VALUES 
  ('Downtown Store', '123 Main St'),
  ('Uptown Store', '456 North Ave'),
  ('Suburban Store', '789 Suburb Ln');

-- Insert 4 employees
INSERT INTO employee (firstName, lastName, userName, password, role, bonus_percentage, hourlyRate)
VALUES
  ('Rudy', 'Gobert', 'ot', '1', 'employee', 1.0, 15.50),
  ('Jane', 'Smith', 'jsmith', 'word456', 'employee', 1.0, 16.00),
  ('Carlos', 'Garcia', 'cgarcia', 'cpass', 'employee', 1.0, 14.75),
  ('Emily', 'Nguyen', 'enguyen', 'emp789', 'employee', 1.0, 15.25);

-- Insert 2 owners
INSERT INTO employee (firstName, lastName, userName, password, role, bonus_percentage, hourlyRate)
VALUES
  ('Olivia', 'Brown', 'obrown', 'ownerpass1', 'owner', 2.0, 0.00),
  ('Bronny', 'James', 'o', '1', 'owner', 2.0, 0.00);


------------------------
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-03-22 01:55:34', '2025-03-22 07:03:46', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 1, '2025-03-21 11:34:02', '2025-03-21 20:45:01', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 1, '2025-03-26 22:02:46', '2025-03-27 02:45:50', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-03-28 13:27:43', '2025-03-28 18:26:54', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-03-27 03:09:51', '2025-03-27 12:32:40', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-03-22 00:55:23', '2025-03-22 09:27:10', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 3, '2025-04-07 11:14:44', '2025-04-07 15:29:48', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-14 01:41:46', '2025-04-14 11:29:48', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-04-01 15:13:33', '2025-04-01 20:44:08', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-04 13:12:41', '2025-04-04 19:11:45', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-03-23 03:09:41', '2025-03-23 12:38:38', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 2, '2025-04-20 08:23:58', '2025-04-20 13:03:53', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 2, '2025-04-02 00:29:16', '2025-04-02 07:27:03', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 2, '2025-03-22 00:31:24', '2025-03-22 07:39:03', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 1, '2025-03-25 11:32:43', '2025-03-25 16:56:50', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-04-09 03:55:33', '2025-04-09 11:28:45', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 1, '2025-04-06 18:58:34', '2025-04-06 23:35:57', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-04-02 22:51:56', '2025-04-03 04:03:35', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 1, '2025-04-02 03:38:35', '2025-04-02 09:35:44', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 1, '2025-04-05 17:39:37', '2025-04-05 23:32:55', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 3, '2025-04-01 07:38:14', '2025-04-01 16:43:33', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-16 23:31:39', '2025-04-17 05:20:29', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 2, '2025-03-25 10:50:37', '2025-03-25 17:25:09', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 1, '2025-03-31 08:06:53', '2025-03-31 13:58:57', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-03-22 12:27:34', '2025-03-22 20:15:24', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 3, '2025-04-06 04:57:22', '2025-04-06 14:08:07', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-07 23:23:09', '2025-04-08 06:24:46', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-03-25 07:35:46', '2025-03-25 12:13:50', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 2, '2025-04-18 05:23:46', '2025-04-18 12:11:42', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-04-06 17:05:21', '2025-04-07 01:23:41', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 1, '2025-03-24 03:50:11', '2025-03-24 09:47:49', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 3, '2025-03-30 02:16:17', '2025-03-30 10:21:35', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-04-10 06:08:53', '2025-04-10 15:59:12', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 2, '2025-03-28 13:53:09', '2025-03-28 19:40:05', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 3, '2025-04-12 00:52:16', '2025-04-12 08:46:40', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 2, '2025-04-09 00:59:56', '2025-04-09 09:14:21', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-03-27 17:48:51', '2025-03-28 01:10:14', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-03-26 05:11:39', '2025-03-26 14:39:01', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 2, '2025-03-26 12:15:29', '2025-03-26 18:38:32', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 2, '2025-04-06 23:00:46', '2025-04-07 05:18:05', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-03-31 13:57:48', '2025-03-31 19:00:52', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-12 00:59:06', '2025-04-12 06:01:45', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-04-17 04:05:01', '2025-04-17 09:49:37', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-18 19:44:53', '2025-04-19 01:49:03', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 3, '2025-03-31 04:19:35', '2025-03-31 12:37:22', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 2, '2025-04-10 12:05:24', '2025-04-10 16:20:40', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-03-30 11:11:55', '2025-03-30 19:09:55', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-05 19:43:49', '2025-04-06 04:52:18', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 3, '2025-04-08 01:48:46', '2025-04-08 09:19:24', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 3, '2025-04-17 00:16:48', '2025-04-17 05:59:07', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-04 15:41:19', '2025-04-04 22:30:44', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 2, '2025-04-11 15:00:08', '2025-04-11 20:09:23', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-04-13 03:44:31', '2025-04-13 08:22:20', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-04-04 04:00:34', '2025-04-04 10:09:33', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-03-27 05:24:48', '2025-03-27 13:53:28', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-03-22 19:58:58', '2025-03-23 00:28:18', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 1, '2025-04-07 13:09:04', '2025-04-07 19:46:38', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 2, '2025-03-26 22:11:13', '2025-03-27 07:57:05', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 1, '2025-04-06 11:55:42', '2025-04-06 20:27:27', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 3, '2025-04-16 11:56:15', '2025-04-16 17:54:48', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 2, '2025-04-04 15:16:21', '2025-04-04 22:15:00', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 3, '2025-03-28 16:46:46', '2025-03-28 23:50:59', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-03-28 03:19:25', '2025-03-28 13:12:12', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-03-27 14:36:25', '2025-03-27 22:27:09', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-12 06:18:00', '2025-04-12 10:59:40', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-04-14 00:42:15', '2025-04-14 10:05:17', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 1, '2025-04-19 01:23:23', '2025-04-19 06:49:03', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-03-22 20:53:35', '2025-03-23 02:10:34', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (2, 1, '2025-04-10 10:44:15', '2025-04-10 16:30:30', 16.00, 16.00);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-04-05 11:14:21', '2025-04-05 17:57:00', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 2, '2025-03-24 12:20:54', '2025-03-24 19:54:06', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (1, 3, '2025-04-11 03:10:00', '2025-04-11 12:16:20', 15.50, 15.50);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 3, '2025-03-22 10:30:36', '2025-03-22 14:36:40', 14.75, 14.75);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (4, 2, '2025-04-17 06:10:45', '2025-04-17 15:15:45', 15.25, 15.25);
INSERT INTO clockTable (employee_id, store_id, clock_in, clock_out, reg_in, reg_out) VALUES (3, 1, '2025-03-31 19:21:04', '2025-04-01 01:13:43', 14.75, 14.75);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Clothing', '2025-04-10', 3, 27, 69.34, 3);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Home Goods', '2025-04-10', 3, 23, 78.48, 2);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Electronics', '2025-03-27', 2, 19, 79.45, 1);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Accessories', '2025-04-18', 2, 21, 94.87, 4);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Clothing', '2025-04-19', 1, 34, 95.48, 2);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Beauty', '2025-04-02', 1, 10, 82.81, 2);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Clothing', '2025-03-30', 2, 41, 58.24, 4);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Clothing', '2025-04-07', 1, 31, 77.73, 3);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Accessories', '2025-03-22', 3, 47, 93.51, 1);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Home Goods', '2025-03-25', 3, 50, 68.61, 2);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Beauty', '2025-03-28', 1, 15, 53.88, 1);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Clothing', '2025-03-23', 2, 2, 65.0, 3);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Electronics', '2025-04-18', 2, 34, 47.01, 4);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Accessories', '2025-04-04', 3, 27, 68.35, 2);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Clothing', '2025-03-29', 2, 39, 34.96, 2);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Electronics', '2025-04-06', 3, 24, 20.62, 3);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Home Goods', '2025-03-27', 3, 29, 91.54, 4);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Accessories', '2025-03-26', 2, 40, 53.27, 1);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Electronics', '2025-04-14', 1, 44, 99.76, 3);
INSERT INTO merchandise (merchandise_type, merchandise_date, store_id, quantity, unitPrice, employee_id) VALUES ('Beauty', '2025-04-07', 1, 14, 40.02, 3);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Travel', '2025-03-28', 2, 428.5, 1);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Meal', '2025-04-11', 2, 131.35, 1);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Travel', '2025-04-19', 4, 92.1, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Travel', '2025-03-28', 3, 84.4, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Utility', '2025-03-27', 3, 332.95, 3);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Utility', '2025-04-05', 3, 235.49, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Utility', '2025-04-17', 1, 36.81, 3);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Travel', '2025-04-09', 1, 152.29, 3);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Maintenance', '2025-04-11', 1, 299.68, 3);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Meal', '2025-04-04', 2, 496.93, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Supplies', '2025-04-12', 1, 411.77, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Meal', '2025-04-20', 2, 493.93, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Meal', '2025-04-07', 3, 104.89, 3);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Meal', '2025-04-07', 2, 169.34, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Supplies', '2025-03-27', 3, 320.36, 3);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Supplies', '2025-04-14', 4, 472.39, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Supplies', '2025-03-27', 2, 307.77, 1);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Travel', '2025-03-29', 3, 345.58, 1);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Utility', '2025-04-01', 2, 388.23, 2);
INSERT INTO expenses (expense_type, expense_date, employee_id, expense_value, store_id) VALUES ('Utility', '2025-03-29', 3, 473.58, 2);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Omega Partners', 873.21, '2025-04-24', '2025-04-07', 'paid', '2025-04-12', 2, 873.21);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Omega Partners', 3790.83, '2025-04-30', '2025-04-01', 'unpaid', NULL, 3, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Omega Partners', 1174.84, '2025-05-10', '2025-04-20', 'paid', '2025-05-04', 3, 1174.84);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Prime Trade', 2393.83, '2025-05-08', '2025-04-14', 'unpaid', NULL, 3, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Pioneer Ltd', 342.36, '2025-04-13', '2025-03-22', 'paid', '2025-04-12', 2, 342.36);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Pioneer Ltd', 2536.02, '2025-04-25', '2025-04-10', 'unpaid', NULL, 1, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('ABC Corp', 2797.32, '2025-04-18', '2025-03-23', 'unpaid', NULL, 3, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('XYZ LLC', 3453.48, '2025-04-26', '2025-04-01', 'unpaid', NULL, 3, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Horizon LLC', 1339.27, '2025-04-23', '2025-04-06', 'unpaid', NULL, 2, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('XYZ LLC', 1441.09, '2025-04-21', '2025-03-28', 'paid', '2025-04-11', 2, 1441.09);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Pioneer Ltd', 4775.06, '2025-04-30', '2025-04-08', 'paid', '2025-04-16', 3, 4775.06);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Atlas Co', 4047.51, '2025-04-19', '2025-04-02', 'paid', '2025-04-19', 2, 4047.51);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('ABC Corp', 2567.46, '2025-05-13', '2025-04-17', 'unpaid', NULL, 1, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Atlas Co', 4380.52, '2025-04-29', '2025-04-11', 'paid', '2025-04-13', 2, 4380.52);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Horizon LLC', 4319.35, '2025-04-28', '2025-04-03', 'paid', '2025-04-24', 1, 4319.35);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('XYZ LLC', 2683.13, '2025-04-29', '2025-04-10', 'unpaid', NULL, 2, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Tech Solutions', 2322.85, '2025-05-03', '2025-04-04', 'paid', '2025-05-02', 2, 2322.85);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Prime Trade', 1369.93, '2025-04-07', '2025-03-23', 'unpaid', NULL, 2, 0.0);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('Atlas Co', 2049.94, '2025-04-24', '2025-04-02', 'paid', '2025-04-24', 2, 2049.94);
INSERT INTO Invoice (company_name, amount, due_date, recieved_date, paid_status, payment_date, store_id, amount_paid) VALUES ('XYZ LLC', 4237.24, '2025-04-16', '2025-03-23', 'unpaid', NULL, 3, 0.0);