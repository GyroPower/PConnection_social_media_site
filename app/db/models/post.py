from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False, default="")
    media = Column(LargeBinary, nullable=True)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    create_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    votes = Column(Integer, server_default="0", nullable=False)
    owner = relationship("User", back_populates="post")
