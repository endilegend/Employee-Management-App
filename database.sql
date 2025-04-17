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
);

CREATE TABLE IF NOT EXISTS expenses (
                                        expense_id INT PRIMARY KEY AUTO_INCREMENT,
                                        expense_type VARCHAR(150),
                                        expense_date DATE,
                                        employee_id INT,
                                        expense_value DECIMAL(10,2),
                                        store_id INT,
                                        FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
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
                                              firstName VARCHAR(15),
                                              lastName VARCHAR(15),
                                              store_name VARCHAR(25),
                                              credit DECIMAL(10, 2),
                                              cash_in_envelope DECIMAL(10, 2),
                                              expense DECIMAL(10, 2),
                                              comments TEXT,
                                              employee_id INT,
                                              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                              FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
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
                                       amount_due DECIMAL(10,2),
                                       due_date DATE,
                                       recieved_date DATE,
                                       paid_status ENUM('paid', 'unpaid'),
                                       payment_date DATE,
                                       store_id INT,
                                       FOREIGN KEY (store_id) REFERENCES Store(store_id)
);

CREATE TABLE IF NOT EXISTS Bonuses (
                                       bonus_id INT AUTO_INCREMENT PRIMARY KEY,
                                       employee_id INT,
                                       store_id INT,
                                       week_start DATE,
                                       week_end DATE,
                                       total_sales DECIMAL(10,2),
                                       bonus_percentage DECIMAL(10,2),
                                       FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
                                       FOREIGN KEY (store_id) REFERENCES Store(store_id)
);
