from flask import Flask, request, redirect, url_for, render_template, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 假设的管理员用户信息
ADMIN_USER = 'admin'
ADMIN_PASSWORD = 'password'

# 加载或保存产品信息的函数
def load_products():
    try:
        with open('products.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_products(products):
    with open('products.json', 'w') as file:
        json.dump(products, file)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    products = load_products()
    return render_template('manage.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_product():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    name = request.form['name']
    products = load_products()
    products.append({'name': name})
    save_products(products)
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_product():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    name = request.form['name']
    products = load_products()
    products = [product for product in products if product['name'] != name]
    save_products(products)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
