from flask import Flask, jsonify, request, abort, send_file
import json
import os

app = Flask(__name__)

class Product:
    def __init__(self, id, name, description, icon):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon

products = []
product_id_counter = 0


def get_json_product(product):
    json_view =  {
        "id": product.id,
        "name": product.name,
        "description": product.description
    }
    return json_view

@app.route('/product', methods=['POST'])
def create_product():
    global product_id_counter
    data = json.loads(request.data)
    product = Product(id=product_id_counter,
                      name=data['name'],
                      description=data['description'],
                      icon=None)
    products.append(product)
    product_id_counter += 1
    return jsonify(get_json_product(product))

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        abort(404)
    return jsonify(get_json_product(product))

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        abort(404)
    data = json.loads(request.data)
    if 'name' in data and type(data['name']) != str:
        abort(400)
    if 'description' in data and type(data['description']) is not str:
        abort(400)
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    return jsonify(get_json_product(product))

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        abort(404)
    products.remove(product)
    return jsonify(get_json_product(product))

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify([get_json_product(p) for p in products])

@app.route('/product/<int:product_id>/image', methods=['POST'])
def upload_image(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        abort(404)
    file = request.files['icon']
    if file:
        filename = f"{product_id}_{file.filename}"
        file.save(os.path.join("images", filename))
        product.icon = filename
        return jsonify({})
    else:
        abort(400)

@app.route('/product/<int:product_id>/image', methods=['GET'])
def get_image(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product is None or product.icon is None:
        abort(404)
    return send_file(os.path.join("images", product.icon))

if __name__ == '__main__':
    app.run(debug=True)
