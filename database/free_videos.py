from asyncpg import Connection
from pydantic import BaseModel
from typing import List, Optional

class freeVideosModel_getVideos(BaseModel):
    video_id: int
    message_chat_id: int
    message_message_id: int
    video_url: str

class free_videos:
    def __init__(self):
        self.db = None

    def connect(self, db: Connection):
        self.db = db

    async def create_table(self):
        async with self.db.acquire() as connection:
            await connection.execute('''CREATE TABLE IF NOT EXISTS free_videos (
                video_id SERIAL PRIMARY KEY,
                message_chat_id BIGINT NOT NULL,
                message_message_id INTEGER NOT NULL,
                video_url TEXT NOT NULL
            )''')

    async def getVideo(self, video_id: int) -> Optional[freeVideosModel_getVideos]:
        async with self.db.acquire() as connection:
            row = await connection.fetchrow('''SELECT * FROM free_videos WHERE video_id = $1''', video_id)
            return freeVideosModel_getVideos.parse_obj(dict(row))

    async def addVideo(self, chat_id: int, message_id: int, video_url: str):
        async with self.db.acquire() as connection:
            await connection.execute('''INSERT INTO free_videos (message_chat_id, message_message_id, video_url)
            VALUES ($1, $2, $3)''', chat_id, message_id, video_url)

    async def getVideos(self) -> List[freeVideosModel_getVideos]:
        async with self.db.acquire() as connection:
            rows = await connection.fetch('''SELECT * FROM free_videos''')
            return [freeVideosModel_getVideos.parse_obj(dict(row)) for row in rows]

    async def delVideos(self):
        async with self.db.acquire() as connection:
              await connection.execute('''DELETE FROM free_videos''')
