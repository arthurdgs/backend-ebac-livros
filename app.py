from fastapi import FastAPI, HTTPException
app = FastAPI()
livros = {}

# Adicionar livros

@app.post("/adicionar_livro/")
def adicionar_livro(id_livro: int, titulo: str, autor: str, ano_livro: int):
    if id_livro in livros:
        raise HTTPException(status_code=400, detail="Esse livro já existe")
    else:
        livros[id_livro] = { 'título': titulo, 'autor': autor, 'ano_livro': ano_livro }
        return {"message": "Livro adicionado com sucesso"}

@app.get("/livros/")
def listar_livros():
    return {"livros": livros}

@app.put("/atualizar_livro/{id_livro}")
def atualizar_livro(id_livro: int, titulo: str, autor: str, ano_livro: int):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        if titulo:
            livros[id_livro]['título'] = titulo
        if autor:
            livros[id_livro]['autor'] = autor
        if ano_livro:
            livros[id_livro]['ano_livro'] = ano_livro

        return {"message": "Livro atualizado com sucesso"}

@app.delete("/deletar_livro/{id_livro}")
def deletar_livro(id_livro: int):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        del livros[id_livro]
        return {"message": "Livro deletado com sucesso"}
                    