


class LivroDB(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, unique=True, index=True)
    autor = Column(String, index=True)
    ano_livro = Column(Integer)
