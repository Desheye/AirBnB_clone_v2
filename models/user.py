from sqlalchemy import Column, String, DateTime  # Import DateTime here
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from datetime import datetime  # If you are using this for default value


class User(BaseModel, Base):
    """Represents a user in the database.
    Attributes:
        email: The user's email address.
        password: The user's password for login.
        first_name: The user's first name.
        last_name: The user's last name.
    """

    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)  # Example usage of DateTime
    updated_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)  # Example usage of DateTime
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    places = relationship("Place",
                          cascade="all, delete, delete-orphan",
                          backref="user")
    reviews = relationship("Review",
                           cascade="all, delete, delete-orphan",
                           backref="user")
