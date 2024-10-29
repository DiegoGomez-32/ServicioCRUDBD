
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Definir el modelo
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

# Crear la base de datos
with app.app_context():
    db.create_all()

# Crear (Create)
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.id), 201

# Leer (Read)
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{ 'id': item.id, 'name': item.name, 'description': item.description } for item in items])

# Actualizar (Update)
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.json
    item.name = data['name']
    item.description = data.get('description')
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

# Eliminar (Delete)
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item eliminado'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
