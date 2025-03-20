from asyncpg import Connection
from pydantic import BaseModel
from typing import List, Optional
import openpyxl

class payments:
    def __init__(self):
        self.db = None

    def connect(self, db: Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS payments (
                payment_id SERIAL PRIMARY KEY,
                datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                amount NUMERIC(10, 2) NOT NULL
            )''')

    async def add_payment(self, user_id: int, amount: float):
        async with self.db.acquire() as connection:
            if await self.check_payment(user_id):
                await connection.execute('''INSERT INTO payments (user_id, amount) VALUES ($1, $2)''', user_id, amount)

    async def check_payment(self, user_id: int):
        async with self.db.acquire() as connection:
            return await connection.fetchval('''SELECT EXISTS(SELECT * FROM payments WHERE user_id = $1)''', user_id)

    async def get_payments(self) -> str:
        '''Returns xlsx lsit of all payments'''
        file_path = 'payments.xlsx'
        async with self.db.acquire() as connection:
            payments = await connection.fetch('''SELECT * FROM payments''')
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.append(['Payment ID', 'Datetime', 'User ID', 'Amount'])
            for payment in payments:
                worksheet.append([payment['payment_id'], payment['datetime'], payment['user_id'], payment['amount']])
            workbook.save(file_path)
            return file_path

    async def get_payments_count(self):
        async with self.db.acquire() as connection:
            count = await connection.fetchval('''SELECT COUNT(*) FROM payments''')
            summ = await connection.fetchval('''SELECT SUM(amount) FROM payments''')
            return count, summ

