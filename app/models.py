from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

# SQLALCHEMY
# Modelo de COMO SERÁ A TABELA NO BD!
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


