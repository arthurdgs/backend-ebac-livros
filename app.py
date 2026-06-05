from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import optional
app = FastAPI()

class Livro(BaseModel):
    titulo: str
    autor: str
    ano_livro: int

livros = {}

# Adicionar livros

@app.post("/adicionar_livro/")
def adicionar_livro(id_livro: int, livro: Livro):
    if id_livro in livros:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        livros[id_livro] = livro.dict()
        return {"message": "Livro adicionado com sucesso"}

@app.get("/livros/")
def listar_livros():
    return {"livros": livros}

@app.put("/atualizar_livro/{id_livro}")
def atualizar_livro(id_livro: int, livro: Livro):
    meu_livro = livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else: 
        meu_livro [id_livro] = livro.dict()
        return {"message": "Livro atualizado com sucesso"}


@app.delete("/deletar_livro/{id_livro}")
def deletar_livro(id_livro: int):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        del livros[id_livro]
        return {"message": "Livro deletado com sucesso"}
                    