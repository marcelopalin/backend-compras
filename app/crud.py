from sqlalchemy.orm import Session, exc
from sqlalchemy import update
from typing import List, Optional
import types

from sqlalchemy.sql.sqltypes import Boolean

# MODELOS - SQLALCHEMY - PYDANTIC
from . import models, schemas


# FUNÇÕES QUE CONECTANDO BD! E RETORNAN OU INSEREM DADOS

# READ - by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# READ - por e-mail
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# READ
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# CREATE
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "naocriptografado"
    db_user = models.User(nome=user.nome, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # retorna o id! Foi criado agora!
    return db_user # com o id preenchido!


# UPDATE
# https://towardsdatascience.com/build-an-async-python-service-with-fastapi-sqlalchemy-196d8792fa08
def update_user(db: Session, user: schemas.UserUpdate):
    # get the existing data
    db_user = db.query(models.User).filter(models.User.id == user.id).one_or_none()
    if db_user is None:
        return None

    # Update model class variable from requested fields
    for var, value in vars(user).items():
        if var == 'password':
            setattr(db_user, 'hashed_password', value) if value else None
        elif var == 'is_active':
            if isinstance(value, bool):
                setattr(db_user, 'is_active', value)
        else:
            setattr(db_user, var, value) if value else None
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    affected_rows = db.query(schemas.User).filter(schemas.User.id == user_id).delete()
    if not affected_rows:
        raise exc.NoResultFound
    return {"id": str(user_id)}
        


