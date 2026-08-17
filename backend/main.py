from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database import get_connection



app = FastAPI(
    title="BankCore Banking API",
    description="Banking database backend for customer, account and transaction management",
    version="1.0.0"
)
class DepositRequest(BaseModel):
    account_id: int
    amount: float = Field(gt=0)
    reference: str = Field(min_length=3, max_length=50)


class WithdrawalRequest(BaseModel):
    account_id: int
    amount: float = Field(gt=0)
    reference: str = Field(min_length=3, max_length=50)


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float = Field(gt=0)
    reference_out: str = Field(min_length=3, max_length=50)
    reference_in: str = Field(min_length=3, max_length=50)

@app.get("/health")
def health_check():
    connection = get_connection()

    if connection and connection.is_connected():
        connection.close()
        return {
            "status": "healthy",
            "database": "connected"
        }

    return {
        "status": "unhealthy",
        "database": "disconnected"
    }
@app.get("/customers")
def get_customers():
    connection = get_connection()

    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return customers

@app.get("/accounts")
def get_accounts():
    connection = get_connection()

    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM accounts")

    accounts = cursor.fetchall()

    cursor.close()
    connection.close()

    return accounts
@app.get("/transactions")
def get_transactions():
    connection = get_connection()

    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY transaction_date DESC
    """)

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions
@app.get("/accounts/{account_id}/transactions")
def get_account_transactions(account_id: int):
    connection = get_connection()

    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)

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

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions
@app.post("/deposits")
def deposit_money(request: DepositRequest):
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

@app.post("/withdrawals")
def withdraw_money(request: WithdrawalRequest):
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

@app.post("/transfers")
def transfer_money(request: TransferRequest):
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

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
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

    finally:
        cursor.close()
        connection.close()

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
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

    finally:
        cursor.close()
        connection.close()