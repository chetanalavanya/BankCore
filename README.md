# BankCore - Banking Database & REST API

BankCore is a banking database and REST API project built using **MySQL, Python, and FastAPI**.

The project demonstrates relational database design, SQL programming, transaction management, stored procedures, database optimization, and REST API development.

## 🚀 Features

- Customer management
- Bank account management
- Account transaction history
- Deposit operations
- Withdrawal operations
- Fund transfers
- Input validation
- Error handling
- Database transactions with COMMIT and ROLLBACK
- Stored procedures
- SQL views
- Database indexes
- Audit logging
- REST API documentation with Swagger UI

## 🛠️ Technologies Used

- **Python**
- **FastAPI**
- **MySQL**
- **SQL**
- **MySQL Workbench**
- **Pydantic**
- **Uvicorn**
- **python-dotenv**
- **Git & GitHub**

## 🗄️ Database

The BankCore database contains relational banking data such as:

- Customers
- Accounts
- Account Types
- Transactions
- Beneficiaries
- Audit Logs

The database uses:

- Primary Keys
- Foreign Keys
- Constraints
- Joins
- Indexes
- Stored Procedures
- Views
- Transactions
- ACID principles
- Query optimization using `EXPLAIN`

## 🔌 REST API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API and database health |
| GET | `/customers` | Get all customers |
| GET | `/customers/{customer_id}` | Get customer details |
| GET | `/accounts` | Get all accounts |
| GET | `/accounts/{account_id}` | Get account details |
| GET | `/accounts/{account_id}/transactions` | Get account transaction history |
| GET | `/transactions` | Get all transactions |
| POST | `/deposits` | Deposit money |
| POST | `/withdrawals` | Withdraw money |
| POST | `/transfers` | Transfer money |

## 🏗️ Project Architecture

```text
Client
   |
   v
FastAPI REST API
   |
   v
Python Database Layer
   |
   v
MySQL Database
   |
   +-- Customers
   +-- Accounts
   +-- Account Types
   +-- Transactions
   +-- Beneficiaries
   +-- Audit Logs