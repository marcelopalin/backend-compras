from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn


# IMPORTA MODELS, 
from . import crud, models, schemas
from .database import SessionLocal, engine

# Roda 1x na Hora de Subir o Servidor!
# ordem: conecte-se ao BD e Crie as Tabelas
# verifique se houve alteração e Sincronize!
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Cria o Usuário! Retorna um TIPO User
# UserSaida irá filtrar PENEIRA - só deixa passar o nome, email!
# CREATE
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o e-mail já está cadastrado!
    db_user = crud.get_user_by_email(db, email=user.email)
    # Se existe! Lança uma Exception! Forma de tratar o Erro
    # Mensagem limpa
    if db_user:
        raise HTTPException(status_code=400, detail="Email já existe! Escolha outro!")
    user_final = crud.create_user(db=db, user=user)
    return user_final # tem password, tem id


# READ
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# READ ONLY
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# DELETE
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not deleted")
    return db_user


# UPDATE
@app.put("/users/", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found to updated!")
    return db_user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)