import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def get_create_users():
    """
    Возвращает список пользователей.
    Cоздаёт нового пользователя.
    """
    if request.method == 'GET':
        users = [user.to_dict() for user in User.query.all()]
        return jsonify(users)
    if request.method == 'POST':
        try:
            user = json.loads(request.data)
            new_user = User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            )
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            return "Создан новый пользователь в БД!"
        except Exception as e:
            return e


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_create_user(user_id):
    """
    Возвращает пользователя по ID.
    Обновляет данные пользователя по ID.
    """
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Не найден пользователь"
        else:
            return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Не найден пользователь"
        user.id = user_data['id']
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} изменён!"

    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Не найден пользователь"
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} удалён!"


@app.route('/orders', methods=['GET', 'POST'])
def get_create_orders():
    """
    Возвращает список заказов.
    Cоздаёт новый заказ.
    """
    if request.method == 'GET':
        orders = [order.to_dict() for order in Order.query.all()]
        return jsonify(orders)
    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = order['start_date'].split("/")
            month_end, day_end, year_end = order['end_date'].split("/")
            new_order = Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
                end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id'],
            )
            db.session.add(new_order)
            db.session.commit()
            db.session.close()
            return "Создан новый заказ в БД!"
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_create_order(order_id):
    """
    Возвращает заказ по ID.
    Обновляет данные заказа по ID.
    """
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Не найден заказ"
        else:
            return jsonify(order.to_dict())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Не найден заказ"
        month_start, day_start, year_start = order_data['start_date'].split("/")
        month_end, day_end, year_end = order_data['end_date'].split("/")
        order.id = order_data['id']
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(year=int(year_start), month=int(month_start), day=int(day_start))
        order.end_date = datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} изменён!"

    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Не найден заказ"
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} удалён!"


@app.route('/offers', methods=['GET', 'POST'])
def get_create_offers():
    """
    Возвращает список предложений.
    Cоздаёт новое предложение.
    """
    if request.method == 'GET':
        offers = [offer.to_dict() for offer in Offer.query.all()]
        return jsonify(offers)
    if request.method == 'POST':
        try:
            offer = json.loads(request.data)
            new_offer = Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id'],
            )
            db.session.add(new_offer)
            db.session.commit()
            db.session.close()
            return "Создано новое предложение в БД!"
        except Exception as e:
            return e


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def get_create_offer(offer_id):
    """
    Возвращает предложение по ID.
    Обновляет данные предложения по ID.
    """
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Не найдено предложение"
        else:
            return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Не найдено предложение"
        offer.id = offer_data['id']
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение с id {offer_id} изменено!"

    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Не найдено предложение"
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение с id {offer_id} удалено!"


if __name__ == '__main__':
    app.run()
