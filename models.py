# importar bibliotecas

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, select, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///mecanica.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), unique=False, index=True, nullable=False)
    email = Column(String(80), unique=True, index=True, nullable=False)
    cpf = Column(Integer, unique=True, nullable=True, index=True)

    @property
    def __repr__(self):
        return '<pessoa: {}, {}, {}, {}>'.format(self.id, self.nome, self.email, self.cpf)

    def __init__(self, nome, email, cpf, id):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_user(self):
        dados_user = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
        }
        return dados_user


# clase
class Livro(Base):
    __tablename__ = 'livro'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(80), nullable=False, index=True)
    autor = Column(String(80), nullable=False, index=True)
    resumo = Column(String(280), nullable=False, index=True)
    isbn = Column(Integer, unique=True, nullable=False)

    # representação classe
    def verificar_volume(self, volume_movimentacao):
        # o self serve para puxar dele mesmo
        if self.quantidade_produto >= volume_movimentacao:
            return True
        else:
            return False

    def __repr__(self):
        return ('<Livro: título: {} autor: {}  resumo: {}'
                ' isbn:{}>'.format(self.titulo, self.autor, self.resumo, self.isbn))

        # função para salvar no banco

    def save(self):
        db_session.add(self)
        db_session.commit()

        # função para deletar

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_livro(self):
        dados_livro = {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "resumo": self.resumo,
            "isbn": self.isbn
        }
        return dados_livro

        # class empréstimos


class Emprestimo(Base):
    __tablename__ = 'emprestimo'
    id = Column(Integer, primary_key=True, unique=True)
    data_emprestimo = Column(String(40), nullable=False, index=True)
    data_devolucao = Column(String(40), nullable=False, index=True)
    livro_id = Column(Integer, ForeignKey('livro.id'))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

    livro_emprestado = relationship('Livro')
    usuario = relationship('Usuario')

    def __repr__(self):
        return ('<Empréstimo: id: {} data_emprestimo: {}  data_devolucao: {}  livro_emprestado: {} usuario: {} >'.
                format(self.id, self.data_emprestimo, self.data_devolucao, self.livro_id, self.usuario_id))

        # função para salvar no banco

    def save(self):
        db_session.add(self)
        db_session.commit()

        # função para deletar

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_emprestimo(self):
        dados_emprestimo = {
            "id": self.id,
            "data_emprestimo": self.data_emprestimo,
            "data_devolucao": self.data_devolucao,
            "livro_emprestado": self.livro_id,
            "usuario": self.usuario_id,
        }
        return dados_emprestimo

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()