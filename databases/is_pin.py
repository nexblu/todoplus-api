from .config import db_session, init_db
from models import TaskPinDatabase
from .database import Database
import datetime
from sqlalchemy import desc, and_


class IsPinCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id, task_id):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        is_done = TaskPinDatabase(user_id, task_id, created_at, created_at)
        db_session.add(is_done)
        db_session.commit()

    async def delete(self, category, **kwargs):
        pass

    async def get(self, category, **kwargs):
        task_id = kwargs.get("task_id")
        user_id = kwargs.get("user_id")
        if category == "is_pin":
            if (
                data := TaskPinDatabase.query.filter(
                    and_(
                        TaskPinDatabase.task_id == task_id,
                        TaskPinDatabase.user_id == user_id,
                    )
                )
                .order_by(desc(TaskPinDatabase.created_at))
                .first()
            ):
                return True
            return False

    async def update(self, category, **kwargs):
        pass
