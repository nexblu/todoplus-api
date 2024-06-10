from sqlalchemy import (
    Table,
    Column,
    Integer,
    Boolean,
    Float,
    CheckConstraint,
    ForeignKey,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session

mapper_registry = registry()


class WalletDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, created_at, updated_at):
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Wallet '{self.user_id}'>"


wallet_table = Table(
    "wallet",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
    Column("banned_at", Float, nullable=True),
    Column("unbanned_at", Float, nullable=True),
    Column("is_active", Boolean, default=False),
    Column("balance", Float, default=0),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
    CheckConstraint(
        "(banned_at >= 0) OR (banned_at IS NULL)", name="positive_banned_at_or_null"
    ),
    CheckConstraint(
        "(unbanned_at >= 0) OR (unbanned_at IS NULL)",
        name="positive_un_banned_at_or_null",
    ),
)

mapper_registry.map_imperatively(WalletDatabase, wallet_table)
