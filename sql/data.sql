USE bankcore;

-- ============================================================
-- Account Types
-- ============================================================

INSERT INTO account_types (type_name, description)
VALUES
('Savings', 'Savings bank account'),
('Current', 'Current bank account'),
('Salary', 'Salary account');


-- ============================================================
-- Customers
-- ============================================================

INSERT INTO customers
(full_name, email, phone, date_of_birth, address)
VALUES
('Aarav Sharma', 'aarav.sharma@example.com', '9000000001',
 '1998-05-14', 'Hyderabad, Telangana'),

('Priya Reddy', 'priya.reddy@example.com', '9000000002',
 '1997-08-22', 'Bengaluru, Karnataka'),

('Rahul Verma', 'rahul.verma@example.com', '9000000003',
 '1999-02-10', 'Mumbai, Maharashtra'),

('Sneha Rao', 'sneha.rao@example.com', '9000000004',
 '2000-11-05', 'Chennai, Tamil Nadu'),

('Vikram Singh', 'vikram.singh@example.com', '9000000005',
 '1996-03-18', 'Pune, Maharashtra');


-- ============================================================
-- Accounts
-- ============================================================

INSERT INTO accounts
(account_number, customer_id, account_type_id, balance)
VALUES
('100000000001', 1, 1, 19000.00),
('100000000002', 2, 1, 38000.00),
('100000000003', 3, 2, 76000.00),
('100000000004', 4, 3, 30000.00),
('100000000005', 5, 1, 62000.00);


-- ============================================================
-- Initial Transactions
-- ============================================================

INSERT INTO transactions
(account_id, transaction_type, amount, reference_number, description)
VALUES
(1, 'DEPOSIT', 25000.00, 'TXN20260001',
 'Initial account funding'),

(2, 'DEPOSIT', 40000.00, 'TXN20260002',
 'Initial account funding'),

(3, 'DEPOSIT', 75000.00, 'TXN20260003',
 'Initial account funding'),

(4, 'DEPOSIT', 30000.00, 'TXN20260004',
 'Initial account funding'),

(5, 'DEPOSIT', 55000.00, 'TXN20260005',
 'Initial account funding');


-- ============================================================
-- Transfer: Aarav -> Priya
-- ============================================================

INSERT INTO transactions
(account_id, transaction_type, amount, reference_number, description)
VALUES
(1, 'TRANSFER_OUT', 5000.00, 'TXN20260006',
 'Transfer to account 100000000002'),

(2, 'TRANSFER_IN', 5000.00, 'TXN20260007',
 'Transfer from account 100000000001');


-- ============================================================
-- Deposit and Withdrawal
-- ============================================================

INSERT INTO transactions
(account_id, transaction_type, amount, reference_number, description)
VALUES
(1, 'DEPOSIT', 2000.00, 'TXN20260008',
 'Deposit through stored procedure'),

(1, 'WITHDRAWAL', 3000.00, 'TXN20260009',
 'Withdrawal through stored procedure');


-- ============================================================
-- Transfer: Priya -> Rahul
-- ============================================================

INSERT INTO transactions
(account_id, transaction_type, amount, reference_number, description)
VALUES
(2, 'TRANSFER_OUT', 7000.00, 'TXN20260011',
 'Fund transfer to another account'),

(5, 'TRANSFER_IN', 7000.00, 'TXN20260012',
 'Fund transfer received');


-- ============================================================
-- API Deposit
-- ============================================================

INSERT INTO transactions
(account_id, transaction_type, amount, reference_number, description)
VALUES
(1, 'DEPOSIT', 1000.00, 'API-TXN-001',
 'Deposit through REST API');


-- ============================================================
-- API Withdrawal
-- ============================================================

INSERT INTO transactions
(account_id, transaction_type, amount, reference_number, description)
VALUES
(1, 'WITHDRAWAL', 2000.00, 'API-TXN-002',
 'Withdrawal through REST API');


-- ============================================================
-- API Transfer: Priya -> Rahul
-- ============================================================

INSERT INTO transactions
(account_id, transaction_type, amount, reference_number, description)
VALUES
(2, 'TRANSFER_OUT', 1000.00, 'API-TXN-003',
 'Transfer through REST API'),

(3, 'TRANSFER_IN', 1000.00, 'API-TXN-004',
 'Transfer received through REST API');


-- ============================================================
-- Beneficiaries
-- ============================================================

INSERT INTO beneficiaries
(customer_id, beneficiary_name, beneficiary_account_number,
 bank_name, ifsc_code)
VALUES
(1, 'Priya Reddy', '100000000002', 'BankCore Bank', 'BKCB0000001'),

(2, 'Aarav Sharma', '100000000001', 'BankCore Bank', 'BKCB0000002'),

(3, 'Sneha Rao', '100000000004', 'BankCore Bank', 'BKCB0000003'),

(4, 'Vikram Singh', '100000000005', 'BankCore Bank', 'BKCB0000004'),

(5, 'Rahul Verma', '100000000003', 'BankCore Bank', 'BKCB0000005');


-- ============================================================
-- Audit Logs
-- ============================================================

INSERT INTO audit_logs
(customer_id, action, table_name, record_id,
 ip_address, details)
VALUES
(1, 'ACCOUNT_CREATED', 'accounts', '1',
 '127.0.0.1', 'Savings account created for customer'),

(2, 'ACCOUNT_CREATED', 'accounts', '2',
 '127.0.0.1', 'Savings account created for customer'),

(1, 'TRANSFER_INITIATED', 'transactions', 'TXN20260006',
 '127.0.0.1', 'Transferred INR 5000 to account 100000000002'),

(2, 'TRANSFER_RECEIVED', 'transactions', 'TXN20260007',
 '127.0.0.1', 'Received INR 5000 from account 100000000001'),

(1, 'BENEFICIARY_ADDED', 'beneficiaries', '1',
 '127.0.0.1', 'Beneficiary Priya Reddy added');