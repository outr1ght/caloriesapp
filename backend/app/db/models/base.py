from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class ModelBase(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __abstract__ = True
