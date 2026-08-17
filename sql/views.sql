USE bankcore;

-- ============================================================
-- Customer Account Summary
-- ============================================================

CREATE OR REPLACE VIEW customer_account_summary AS
SELECT
    c.customer_id,
    c.full_name,
    c.email,
    c.phone,
    a.account_id,
    a.account_number,
    at.type_name AS account_type,
    a.balance,
    a.status AS account_status,
    a.opened_at
FROM customers c
JOIN accounts a
    ON c.customer_id = a.customer_id
JOIN account_types at
    ON a.account_type_id = at.account_type_id;


-- ============================================================
-- Transaction Statement
-- ============================================================

CREATE OR REPLACE VIEW transaction_statement AS
SELECT
    t.transaction_id,
    c.customer_id,
    c.full_name,
    a.account_number,
    t.transaction_type,
    t.amount,
    t.reference_number,
    t.description,
    t.status,
    t.transaction_date
FROM transactions t
JOIN accounts a
    ON t.account_id = a.account_id
JOIN customers c
    ON a.customer_id = c.customer_id;