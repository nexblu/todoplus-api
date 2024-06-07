from .config import db_session, init_db
from models import IsDoneDatabase, TodoListDatabase, UserDatabase
from .database import Database
import datetime
from sqlalchemy import desc, and_
from utils import TaskNotFound
from .user import UserCRUD


class IsDoneCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()
        self.user_database = UserCRUD()

    async def insert(self, user_id, task_id):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        is_done = IsDoneDatabase(user_id, task_id, created_at, created_at)
        db_session.add(is_done)
        db_session.commit()

    async def delete(self, category, **kwargs):
        pass

    async def get(self, category, **kwargs):
        task_id = kwargs.get("task_id")
        user_id = kwargs.get("user_id")
        if category == "is_done":
            if (
                data := IsDoneDatabase.query.filter(
                    and_(
                        IsDoneDatabase.task_id == task_id,
                        IsDoneDatabase.user_id == user_id,
                    )
                )
                .order_by(desc(IsDoneDatabase.created_at))
                .first()
            ):
                return True
            return False
        if category == "all":
            if (
                data := db_session.query(UserDatabase, TodoListDatabase, IsDoneDatabase)
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(IsDoneDatabase)
                .filter(UserDatabase.id == user_id)
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                return data
            raise TaskNotFound

    async def update(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        email = kwargs.get("email")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if category == "all":
            if todo := TodoListDatabase.query.filter(
                TodoListDatabase.user_id == user_id
            ).all():
                for data in todo:
                    is_done = IsDoneDatabase(user_id, data.id, created_at, created_at)
                    data.updated_at = created_at
                    db_session.add(is_done)
                db_session.commit()
                await self.user_database.update(
                    "updated_at", updated_at=created_at, email=email
                )
                return
            raise TaskNotFound
