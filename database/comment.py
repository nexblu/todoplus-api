from .config import db_session, init_db
from models import CommentDatabase
from .database import Database
from sqlalchemy import desc, and_
from utils import CommentNotFound


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
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        if catageory == "task_id":
            result = CommentDatabase.query.filter(
                and_(
                    CommentDatabase.user_id == user_id,
                    CommentDatabase.task_id == task_id,
                )
            ).delete()
            db_session.commit()
            if not result:
                raise CommentNotFound

    async def get(self, catageory, **kwargs):
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        if catageory == "task_id":
            if (
                data := CommentDatabase.query.filter(
                    and_(
                        CommentDatabase.user_id == user_id,
                        CommentDatabase.task_id == task_id,
                    )
                )
                .order_by(desc(CommentDatabase.created_at))
                .all()
            ):
                return data
            raise CommentNotFound
