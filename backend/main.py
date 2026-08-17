from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import get_connection


app = FastAPI(
    title="BankCore Banking API",
    description=(
        "REST API for banking customer, account and transaction management "
        "using FastAPI and MySQL."
    ),
    version="1.0.0"
)


# ============================================================
# Request Models
# ============================================================

class DepositRequest(BaseModel):
    account_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0)
    reference: str = Field(min_length=3, max_length=50)


class WithdrawalRequest(BaseModel):
    account_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0)
    reference: str = Field(min_length=3, max_length=50)


class TransferRequest(BaseModel):
    from_account_id: int = Field(gt=0)
    to_account_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0)
    reference_out: str = Field(min_length=3, max_length=50)
    reference_in: str = Field(min_length=3, max_length=50)


# ============================================================
# Health Check
# ============================================================

@app.get("/health", tags=["System"])
def health_check():
    """Check whether the API can connect to MySQL."""

    connection = get_connection()

    if not connection:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }

    try:
        if connection.is_connected():
            return {
                "status": "healthy",
                "database": "connected"
            }

        return {
            "status": "unhealthy",
            "database": "disconnected"
        }

    finally:
        connection.close()


# ============================================================
# Customers
# ============================================================

@app.get("/customers", tags=["Customers"])
def get_customers():
    """Return all customers."""

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                customer_id,
                full_name,
                email,
                phone,
                date_of_birth,
                address,
                created_at,
                status
            FROM customers
            ORDER BY customer_id
        """)

        return cursor.fetchall()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve customers: {str(e)}"
        )

    finally:
        cursor.close()
        connection.close()


@app.get("/customers/{customer_id}", tags=["Customers"])
def get_customer(customer_id: int):
    """Return a customer by ID."""

    if customer_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Customer ID must be greater than zero"
        )

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                customer_id,
                full_name,
                email,
                phone,
                date_of_birth,
                address,
                created_at,
                status
            FROM customers
            WHERE customer_id = %s
        """, (customer_id,))

        customer = cursor.fetchone()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return customer

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve customer: {str(e)}"
        )

    finally:
        cursor.close()
        connection.close()


# ============================================================
# Accounts
# ============================================================

@app.get("/accounts", tags=["Accounts"])
def get_accounts():
    """Return all bank accounts."""

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                account_id,
                account_number,
                customer_id,
                account_type_id,
                balance,
                opened_at,
                status
            FROM accounts
            ORDER BY account_id
        """)

        return cursor.fetchall()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve accounts: {str(e)}"
        )

    finally:
        cursor.close()
        connection.close()


@app.get("/accounts/{account_id}", tags=["Accounts"])
def get_account(account_id: int):
    """Return detailed account information."""

    if account_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Account ID must be greater than zero"
        )

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.account_id,
                a.account_number,
                c.full_name,
                at.type_name AS account_type,
                a.balance,
                a.status,
                a.opened_at
            FROM accounts a
            JOIN customers c
                ON a.customer_id = c.customer_id
            JOIN account_types at
                ON a.account_type_id = at.account_type_id
            WHERE a.account_id = %s
        """, (account_id,))

        account = cursor.fetchone()

        if not account:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        return account

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve account: {str(e)}"
        )

    finally:
        cursor.close()
        connection.close()


# ============================================================
# Transactions
# ============================================================

@app.get("/transactions", tags=["Transactions"])
def get_transactions():
    """Return all transactions."""

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                transaction_id,
                account_id,
                transaction_type,
                amount,
                reference_number,
                description,
                status,
                transaction_date
            FROM transactions
            ORDER BY transaction_date DESC
        """)

        return cursor.fetchall()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve transactions: {str(e)}"
        )

    finally:
        cursor.close()
        connection.close()


@app.get(
    "/accounts/{account_id}/transactions",
    tags=["Transactions"]
)
def get_account_transactions(account_id: int):
    """Return transaction history for a specific account."""

    if account_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Account ID must be greater than zero"
        )

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                transaction_id,
                account_id,
                transaction_type,
                amount,
                reference_number,
                description,
                status,
                transaction_date
            FROM transactions
            WHERE account_id = %s
            ORDER BY transaction_date DESC
        """, (account_id,))

        return cursor.fetchall()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve transaction history: {str(e)}"
        )

    finally:
        cursor.close()
        connection.close()


# ============================================================
# Deposit
# ============================================================

@app.post("/deposits", tags=["Banking Operations"])
def deposit_money(request: DepositRequest):
    """Deposit money into an account."""

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:
        cursor.callproc(
            "deposit_money",
            (
                request.account_id,
                request.amount,
                request.reference
            )
        )

        connection.commit()

        return {
            "message": "Deposit successful",
            "account_id": request.account_id,
            "amount": request.amount,
            "reference": request.reference
        }

    except Exception as e:
        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        cursor.close()
        connection.close()


# ============================================================
# Withdrawal
# ============================================================

@app.post("/withdrawals", tags=["Banking Operations"])
def withdraw_money(request: WithdrawalRequest):
    """Withdraw money from an account."""

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:
        cursor.callproc(
            "withdraw_money",
            (
                request.account_id,
                request.amount,
                request.reference
            )
        )

        connection.commit()

        return {
            "message": "Withdrawal successful",
            "account_id": request.account_id,
            "amount": request.amount,
            "reference": request.reference
        }

    except Exception as e:
        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        cursor.close()
        connection.close()


# ============================================================
# Fund Transfer
# ============================================================

@app.post("/transfers", tags=["Banking Operations"])
def transfer_money(request: TransferRequest):
    """Transfer money between two accounts."""

    if request.from_account_id == request.to_account_id:
        raise HTTPException(
            status_code=400,
            detail="Source and destination accounts must be different"
        )

    connection = get_connection()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:
        cursor.callproc(
            "transfer_money",
            (
                request.from_account_id,
                request.to_account_id,
                request.amount,
                request.reference_out,
                request.reference_in
            )
        )

        connection.commit()

        return {
            "message": "Transfer successful",
            "from_account_id": request.from_account_id,
            "to_account_id": request.to_account_id,
            "amount": request.amount,
            "reference_out": request.reference_out,
            "reference_in": request.reference_in
        }

    except Exception as e:
        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        cursor.close()
        connection.close()