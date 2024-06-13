from .config import db_session, init_db
from models import CommentDatabase
from .database import Database


class CommentCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id, comment, task_id, created_at, updated_at):
        comment_database = CommentDatabase(
            user_id, comment, task_id, created_at, updated_at
        )
        db_session.add(comment_database)
        db_session.commit()

    async def update(self, catageory, **kwargs):
        pass

    async def delete(self, catageory, **kwargs):
        pass

    async def get(self, catageory, **kwargs):
        pass
