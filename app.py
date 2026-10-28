from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()
livros = {}


DATABASE_URL = "sqlite:///./biblioteca.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class LivroDB(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key = True)
    titulo = Column (String, unique = True , index = True )
    autor = Column ( String , index = True )
    ano_livro = Column (Integer)

class Livro(BaseModel):
    titulo: str
    autor: str
    ano_livro: int


Base.metadata.create_all(bind=engine)


def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Adicionar livros

@app.post("/adicionar_livro/")
def adicionar_livro(livro: Livro, db: Session = Depends (sessao_db)):

    db_livro = db.query(LivroDB).filter(LivroDB.titulo == livro.titulo).first()

    if db_livro:
        raise HTTPException(status_code=400, detail = 'Livro já cadastrado')

    novo_livro = LivroDB ( titulo = livro.titulo , autor = livro.autor, ano_livro = livro.ano_livro)

    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    return {'message:' 'Livro Cadastrado com sucesso'}

# listar livros

@app.get("/livros/")
def listar_livros(ordenar_livros: int = 1, page: int = 1 , size: int = 10, db: Session = Depends(sessao_db)):
    if page < 1 or size < 1: 
        raise HTTPException (
            status_code = 400, detail = 'Page ou Size estão com valores inválidos'
        )
    start = (page - 1) * size 
    end = start + size

    if ordenar_livros == 1: 
        db_livro = db.query(LivroDB).order_by(LivroDB.titulo).offset(start).limit(size).all()

    elif ordenar_livros == 2: 
        db_livro = db.query(LivroDB).order_by(LivroDB.autor).offset(start).limit(size).all()

    total_livros = db.query(LivroDB).count()

    if not db_livro: 
        return {'message:' 'Nenhum Livro cadastrado'}

    return {
        'page': page,
        'size': size,
        'total': total_livros,
        'Livros': [{"Livro": livro.titulo, "autor": livro.autor, "Ano": livro.ano_livro, "id": livro.id } for livro in db_livro]
        
    }

    

# Atualizar livros 

@app.put("/atualizar_livro/{id_livro}")
def atualizar_livro(id_livro: int, livro: Livro, db: Session = Depends(sessao_db)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()

    if not db_livro:
        raise HTTPException (
            status_code = 404, detail = 'Livro não encontrado'
        )

    else: 
        db_livro.titulo = livro.titulo
        db_livro.autor = livro.autor 
        db_livro.ano_livro = livro.ano_livro

        db.commit()
        db.refresh(db_livro)

        return {"message": f"As informações do livro '{livro.titulo}' foram atualizadas com sucesso"}
    
# Excluir livros 

@app.delete("/deletar_livro/{id_livro}")
def deletar_livro(id_livro: int, db: Session = Depends(sessao_db)):
   db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()

   if not db_livro:
       raise HTTPException ( 
           status_code = 404, detail = 'Livro não encontrado'
       )

   db.delete(db_livro)
   db.commit() 

   return {"message": f" O livro foi excluído com sucesso"}    