from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, Boolean, Text

from models.base_class import Base


class Test(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_test: Mapped[bool] = mapped_column(Boolean, default=False)
