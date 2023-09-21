#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_as_ascii = False  # Ensure non-ASCII characters are not escaped in JSON responses

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_serialized), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return jsonify({'error': 'Bakery not found'}), 404
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    by_price = BakedGood.query.order_by(BakedGood.price).all()
    by_price_serialized = [bg.to_dict() for bg in by_price]
    return jsonify(by_price_serialized), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive is None:
        return jsonify({'error': 'No baked goods found'}), 404
    return jsonify(most_expensive.to_dict()), 200

if __name__ == '__main__':
    app.run(port=555, debug=True)
