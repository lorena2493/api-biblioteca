from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///mecanica.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(Integer, nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    def __repr__(self):
        return f'<Cliente(id= {self.id}, \n nome={self.nome}, \n cpf={self.cpf}, \n telefone={self.telefone})>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'endereco': self.endereco
        }


class Veiculo(Base):
    __tablename__ = 'veiculo'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    placa = Column(String, nullable=False, unique=True)
    ano_fabricacao = Column(Integer, nullable=False)
    cliente = relationship('Cliente')

    def __repr__(self):
        return (f'<Veiculo(id ={self.id}, \n modelo={self.modelo}, \n placa={self.placa},'
                f' \n cliente_id={self.cliente_id}, \n ano_fabricacao={self.ano_fabricacao})>')

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'marca': self.marca,
            'modelo': self.modelo,
            'placa': self.placa,
            'ano_fabricacao': self.ano_fabricacao
        }


class OrdemServico(Base):
    __tablename__ = 'ordem_servico'
    id = Column(Integer, primary_key=True)
    veiculo_id = Column(Integer, ForeignKey('veiculo.id'), nullable=False)
    data_abertura = Column(Date, nullable=False)
    descricao_servico = Column(String, nullable=False)
    status = Column(String, nullable=False)
    valor_estimado = Column(Float, nullable=False)
    veiculo = relationship('Veiculo')

    def __repr__(self):
        return (f'<OrdemServico(id= {self.id}, \n veiculo_id={self.veiculo_id}, \n data_abertura={self.data_abertura},'
                f' \n descricao_servico={self.descricao_servico}, \n status={self.status}, \n valor_estimado={self.valor_estimado})>')

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'veiculo_id': self.veiculo_id,
            'data_abertura': self.data_abertura,
            'descricao_servico': self.descricao_servico,
            'status': self.status,
            'valor_estimado': self.valor_estimado,
            'veiculo': self.veiculo
        }


def init_db():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
