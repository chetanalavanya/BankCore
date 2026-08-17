USE bankcore;

-- ============================================================
-- Deposit Procedure
-- ============================================================

DELIMITER $$

CREATE PROCEDURE deposit_money(
    IN p_account_id INT,
    IN p_amount DECIMAL(15,2),
    IN p_reference VARCHAR(50)
)
BEGIN
    DECLARE v_status VARCHAR(20);

    START TRANSACTION;

    SELECT status
    INTO v_status
    FROM accounts
    WHERE account_id = p_account_id
    FOR UPDATE;

    IF v_status IS NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Account not found';

    ELSEIF v_status <> 'ACTIVE' THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Account is not active';

    ELSEIF p_amount <= 0 THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Deposit amount must be greater than zero';

    ELSE
        UPDATE accounts
        SET balance = balance + p_amount
        WHERE account_id = p_account_id;

        INSERT INTO transactions
        (account_id, transaction_type, amount, reference_number, description)
        VALUES
        (
            p_account_id,
            'DEPOSIT',
            p_amount,
            p_reference,
            'Deposit through stored procedure'
        );

        COMMIT;
    END IF;
END$$

DELIMITER ;


-- ============================================================
-- Withdrawal Procedure
-- ============================================================

DELIMITER $$

CREATE PROCEDURE withdraw_money(
    IN p_account_id INT,
    IN p_amount DECIMAL(15,2),
    IN p_reference VARCHAR(50)
)
BEGIN
    DECLARE v_balance DECIMAL(15,2);
    DECLARE v_status VARCHAR(20);

    START TRANSACTION;

    SELECT balance, status
    INTO v_balance, v_status
    FROM accounts
    WHERE account_id = p_account_id
    FOR UPDATE;

    IF v_status IS NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Account not found';

    ELSEIF v_status <> 'ACTIVE' THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Account is not active';

    ELSEIF p_amount <= 0 THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Withdrawal amount must be greater than zero';

    ELSEIF v_balance < p_amount THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Insufficient balance';

    ELSE
        UPDATE accounts
        SET balance = balance - p_amount
        WHERE account_id = p_account_id;

        INSERT INTO transactions
        (account_id, transaction_type, amount, reference_number, description)
        VALUES
        (
            p_account_id,
            'WITHDRAWAL',
            p_amount,
            p_reference,
            'Withdrawal through stored procedure'
        );

        COMMIT;
    END IF;
END$$

DELIMITER ;


-- ============================================================
-- Fund Transfer Procedure
-- ============================================================

DELIMITER $$

CREATE PROCEDURE transfer_money(
    IN p_from_account_id INT,
    IN p_to_account_id INT,
    IN p_amount DECIMAL(15,2),
    IN p_reference_out VARCHAR(50),
    IN p_reference_in VARCHAR(50)
)
BEGIN
    DECLARE v_from_balance DECIMAL(15,2);
    DECLARE v_from_status VARCHAR(20);
    DECLARE v_to_status VARCHAR(20);

    START TRANSACTION;

    IF p_from_account_id = p_to_account_id THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
            'Source and destination accounts must be different';

    ELSEIF p_amount <= 0 THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
            'Transfer amount must be greater than zero';

    ELSE

        SELECT balance, status
        INTO v_from_balance, v_from_status
        FROM accounts
        WHERE account_id = p_from_account_id
        FOR UPDATE;

        SELECT status
        INTO v_to_status
        FROM accounts
        WHERE account_id = p_to_account_id
        FOR UPDATE;

        IF v_from_status IS NULL THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Source account not found';

        ELSEIF v_to_status IS NULL THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Destination account not found';

        ELSEIF v_from_status <> 'ACTIVE' THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT =
                'Source account is not active';

        ELSEIF v_to_status <> 'ACTIVE' THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT =
                'Destination account is not active';

        ELSEIF v_from_balance < p_amount THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Insufficient balance';

        ELSE

            UPDATE accounts
            SET balance = balance - p_amount
            WHERE account_id = p_from_account_id;

            UPDATE accounts
            SET balance = balance + p_amount
            WHERE account_id = p_to_account_id;

            INSERT INTO transactions
            (
                account_id,
                transaction_type,
                amount,
                reference_number,
                description
            )
            VALUES
            (
                p_from_account_id,
                'TRANSFER_OUT',
                p_amount,
                p_reference_out,
                'Fund transfer to another account'
            );

            INSERT INTO transactions
            (
                account_id,
                transaction_type,
                amount,
                reference_number,
                description
            )
            VALUES
            (
                p_to_account_id,
                'TRANSFER_IN',
                p_amount,
                p_reference_in,
                'Fund transfer received'
            );

            COMMIT;

        END IF;
    END IF;
END$$

DELIMITER ;