from asyncpg import Connection
from pydantic import BaseModel
from typing import List, Optional
import openpyxl

class users:
    def __init__(self):
        self.db = None

    def connect(self, db: Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT NOT NULL PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )''')

    async def check_user(self, user_id: int) -> bool:
        async with self.db.acquire() as connection:
            return await connection.fetchval('''SELECT EXISTS(SELECT * FROM users WHERE user_id = $1)''', user_id)

    async def add_user(self, user_id: int, username: str, first_name: str, last_name: str):
        if not await self.check_user(user_id):
            async with self.db.acquire() as connection:
                await connection.execute('''INSERT INTO users (user_id, username, first_name, last_name) VALUES ($1, $2, $3, $4)''', user_id, username, first_name, last_name)

    async def get_users_count(self) -> int:
        async with self.db.acquire() as connection:
            return await connection.fetchval('''SELECT COUNT(*) FROM users''')

    async def get_users_list(self) -> str:
        '''Returns xlsx list of all users'''
        async with self.db.acquire() as connection:
            users = await connection.fetch('''SELECT * FROM users''')
            file_path = 'users.xlsx'
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.append(['ID', 'Username', 'First Name', 'Last Name'])
            for user in users:
                if user['username']:
                    worksheet.append([user['user_id'], user['username'], user['first_name'], user['last_name']])
                else:
                    worksheet.append([user['user_id'], '', user['first_name'], user['last_name']])
            workbook.save(file_path)
        return file_path

    async def get_users_ids(self) -> list:
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''SELECT user_id FROM users''')
            return [row['user_id'] for row in rows]
