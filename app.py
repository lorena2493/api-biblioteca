from flask import Flask, request, jsonify
from sqlalchemy import select

from modelsmec import Cliente, Veiculo, OrdemServico, init_db, db_session
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)
spec = FlaskPydanticSpec('flask',
                         title='First API - SENAI',
                         version='1.0.0', )

spec.register(app)


# CLIENTES
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        clientes = select(Cliente)
        result = db_session().execute(clientes).scalars().all()
        listar_clientes = []
        for cliente in result:
            listar_clientes.append({cliente.serialize()})
            return jsonify({'clientes': listar_clientes})
    except ValueError as e:
        return  jsonify({'error': str(e)})


@ app.route('/criar_cliente', methods=['POST'])
def criar_cliente():
    data = request.get_json()
    cliente = Cliente(
        nome=data['nome'],
        cpf=data['cpf'],
        telefone=data['telefone'],
        endereco=data['endereco'],
    )
    cliente.save()
    return jsonify(cliente.serialize()), 201

@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = db_session.execute(select(Cliente).where(Cliente.id == id)).scalar()
    data = request.get_json()
    cliente.nome = data('nome')
    cliente.cpf =data('cpf', cliente.cpf)
    cliente.telefone = data('telefone', cliente.telefone)
    cliente.endereco = data('endereco', cliente.endereco)
    cliente.save()
    return jsonify(cliente.serialize())

@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = db_session.execute(select(Cliente).where(Cliente.id == id)).scalar()
    cliente.delete()
    return jsonify({'message': 'Cliente deletado'})

if __name__ == '__main__':
    app.run(debug=True)
