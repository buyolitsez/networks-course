from flask import Flask, jsonify, request, abort, send_file
import json
import os
import uuid
from hashlib import sha256
import smtplib
import email.message
from threading import Timer

app = Flask(__name__)

class User:
    def __init__(self, email, password_hash, ip_address):
        self.email = email
        self.password_hash = password_hash
        self.token = None
        self.ip_address = ip_address

class Product:
    def __init__(self, id, name, description, icon, owner=None):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.owner = owner

users = {}
tokens = {}
products = []
product_id_counter = 0

timers = {}

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def send_html_email(receiver_address, subject, content, sender_address, sender_pass):
    print('receiver = ', receiver_address)
    print('subject =', subject)
    print('content = ', content)
    print('sender_address = ', sender_address)
    print('sender_pass = ', sender_pass)
    message = email.message.EmailMessage()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    message.add_alternative(content, "html")

    session = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    session.ehlo()
    session.login(sender_address, sender_pass)
    session.send_message(message)
    session.quit()

def start_timer(ip_address):
    if ip_address in timers:
        timers[ip_address].cancel()
    timer = Timer(30, send_welcome_email, [ip_address])
    timers[ip_address] = timer
    timer.start()

def send_welcome_email(ip_address):
    user = next((u for u in users.values() if u.ip_address == ip_address), None)
    if user:
        send_html_email(
            receiver_address=user.email,
            subject="Hello subject",
            content="Glad to see you again!",
            sender_address="steamfakecsgo3@yandex.ru",
            sender_pass='WRONG PASSWORD'
        )

def get_authenticated_user():
    token = request.args.get('token')
    if token:
        return tokens.get(token)
    return None

@app.route('/user/sign-up', methods=['POST'])
def sign_up():
    data = json.loads(request.data)
    email = data['email']
    password = data['password']
    ip_address = request.remote_addr
    if email in users:
        abort(400, description="User already exists")
    password_hash = hash_password(password)
    users[email] = User(email, password_hash, ip_address)
    print('User ip: ', ip_address)
    return jsonify({"message": "User registered successfully"})

@app.route('/user/sign-in', methods=['POST'])
def sign_in():
    data = json.loads(request.data)
    email = data['email']
    password = data['password']
    user = users.get(email)
    if user is None or user.password_hash != hash_password(password):
        abort(401, description="Invalid credentials")
    token = str(uuid.uuid4())
    user.token = token
    tokens[token] = user
    return jsonify({"token": token})

@app.route('/product', methods=['POST'])
def create_product():
    global product_id_counter
    data = json.loads(request.data)
    user = get_authenticated_user()
    ip_address = request.remote_addr
    if not user and any(u.ip_address == ip_address for u in users.values()):
        start_timer(ip_address)
    product = Product(
        id=product_id_counter,
        name=data['name'],
        description=data['description'],
        icon=None,
        owner=user.email if user else None
    )
    products.append(product)
    product_id_counter += 1
    return jsonify(get_json_product(product))

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    user = get_authenticated_user()
    ip_address = request.remote_addr
    if not user and any(u.ip_address == ip_address for u in users.values()):
        start_timer(ip_address)
    product = next((p for p in products if p.id == product_id), None)
    if product is None or (product.owner and product.owner != (user.email if user else None)):
        abort(404)
    return jsonify(get_json_product(product))

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    user = get_authenticated_user()
    ip_address = request.remote_addr
    if not user and any(u.ip_address == ip_address for u in users.values()):
        start_timer(ip_address)
    product = next((p for p in products if p.id == product_id), None)
    if product is None or (product.owner and product.owner != (user.email if user else None)):
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
    user = get_authenticated_user()
    ip_address = request.remote_addr
    if not user and any(u.ip_address == ip_address for u in users.values()):
        start_timer(ip_address)
    product = next((p for p in products if p.id == product_id), None)
    if product is None or (product.owner and product.owner != (user.email if user else None)):
        abort(404)
    products.remove(product)
    return jsonify(get_json_product(product))

@app.route('/products', methods=['GET'])
def get_products():
    user = get_authenticated_user()
    ip_address = request.remote_addr
    if not user and any(u.ip_address == ip_address for u in users.values()):
        start_timer(ip_address)
    if user:
        user_products = [p for p in products if p.owner == user.email or p.owner is None]
    else:
        user_products = [p for p in products if p.owner is None]
    return jsonify([get_json_product(p) for p in user_products])

@app.route('/product/<int:product_id>/image', methods=['POST'])
def upload_image(product_id):
    user = get_authenticated_user()
    ip_address = request.remote_addr
    if not user and any(u.ip_address == ip_address for u in users.values()):
        start_timer(ip_address)
    product = next((p for p in products if p.id == product_id), None)
    if product is None or (product.owner and product.owner != (user.email if user else None)):
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
