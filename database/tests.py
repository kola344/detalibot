from asyncpg import Connection
from pydantic import BaseModel
from typing import List, Optional
import json

class testDataModel(BaseModel):
    question: str
    answers: List[str]
    correct_answer: int

class tests:
    def __init__(self):
        self.db = None

    def connect(self, db: Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS tests (
                test_id SERIAL PRIMARY KEY,
                free_video_id INTEGER NOT NULL REFERENCES free_videos(video_id) ON DELETE CASCADE ON UPDATE CASCADE,
                test_data JSONB
            )''')
    #test data
    # [{question, answers: ['1', '2', '3'], correct_answer: id_answers}]}]

    async def add_test(self, free_video_id: int, test_data: List[dict]):
        async with self.db.acquire() as connection:
            await connection.execute('''INSERT INTO tests (free_video_id, test_data) VALUES ($1, $2)''', free_video_id, json.dumps(test_data))

    async def get_test_data(self, test_id: int):
        async with self.db.acquire() as connection:
            return await connection.fetchval('''SELECT test_data FROM tests WHERE test_id = $1''', test_id)

    async def get_test_data_by_video_id(self, video_id: int):
        async with self.db.acquire() as connection:
            return json.loads(await connection.fetchval('''SELECT test_data FROM tests WHERE free_video_id = $1''', video_id))

    async def update_test_data(self, test_id: int, test_data: List[dict]):
        async with self.db.acquire() as connection:
            await connection.execute('''UPDATE tests SET test_data = $1 WHERE test_id = $2''', test_data, test_id)

    async def check_test_by_video_id(self, video_id: int):
        async with self.db.acquire() as connection:
            return await connection.fetchval('''SELECT 1 FROM tests WHERE free_video_id = $1''', video_id)

    async def del_all_tests_by_video_id(self, video_id: int):
        async with self.db.acquire() as connection:
            await connection.execute('''DELETE FROM tests WHERE free_video_id = $1''', video_id)


