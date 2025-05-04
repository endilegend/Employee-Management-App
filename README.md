# Employee Management Application

A comprehensive desktop application for managing employee clock-ins, clock-outs, and store operations. Built with Python and PyQt5, featuring a MySQL database backend.

## Features

- **User Authentication**

  - Role-based access (Employee, Manager, Owner)
  - Secure login system
  - Session management

- **Employee Features**

  - Clock-in/Clock-out functionality
  - Register balance tracking
  - Shift history viewing
  - Store selection
  - Close register management

- **Store Management**

  - Multiple store support
  - Store-specific operations
  - Register closing procedures

- **Database Integration**
  - MySQL database backend
  - Secure data storage
  - Transaction management

## Prerequisites

- Python 3.x
- MySQL Server
- PyQt5
- Required Python packages:
  ```
  PyQt5
  mysql-connector-python
  pytz
  ```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Employee-Management-App-.git
   cd Employee-Management-App-
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   - Create a new MySQL database
   - Run the `database.sql` script to create the necessary tables
   - Update the database connection details in `sqlConnector.py` if needed

## Database Configuration

The application uses a MySQL database with the following structure:

- **Store**: Store information
- **employee**: Employee details and credentials
- **expenses**: Store expenses tracking
- **merchandise**: Inventory management
- **employee_close**: Register closing records
- **clockTable**: Employee time tracking
- **Invoice**: Store invoice management
- **Payroll**: Employee payroll information

## Usage

1. Start the application:

   ```bash
   python ems.py
   ```

2. Login with your credentials:

   - Username: Your employee username
   - Password: Your assigned password

3. Main Features:
   - **Clock In/Out**: Record your work hours and register balances
   - **Close Register**: Submit daily closing reports
   - **History**: View your clock-in/out history
   - **Store Selection**: Choose your current store location

## Security Features

- Password protection
- Role-based access control
- Secure database connections
- Input validation
- Error handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt5 for the GUI framework
- MySQL for database management
- All contributors who have helped improve this application
