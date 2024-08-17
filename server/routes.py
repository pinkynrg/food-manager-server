from flask import Blueprint, request, jsonify
from server import db
from server.models import Item
from datetime import datetime, timedelta

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET'])
def server_up():
    return 'server is up!', 200

@main_blueprint.route('/items', methods=['POST'])
def add_item():
    data = request.json
    item_name = data['name']
    expiration_date = data['expiration_date']
    user_id = data['user_id']

    expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()
    new_item = Item(name=item_name, expiration_date=expiration_date, user_id=user_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": f"Item {item_name} added with expiration date {expiration_date}"}), 201

@main_blueprint.route('/items', methods=['POST'])
def update_item():
    data = request.json
    item_name = data['name']
    user_id = data['user_id']
    
    item = Item.query.filter_by(name=item_name, user_id=user_id).first()

    if item:
        item.opened_date = datetime.now().date()
        item.expiration_date = item.opened_date + timedelta(days=7)
        db.session.commit()

        return jsonify({"message": f"Item {item_name} updated with new expiration date {item.expiration_date}"}), 200
    else:
        return jsonify({"message": "Item not found"}), 404

@main_blueprint.route('/items/expiring', methods=['GET'])
def items_to_consume():
    user_id = request.args.get('user_id')
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    items = Item.query.filter(Item.user_id == user_id, Item.expiration_date.between(today, tomorrow)).all()
    items_list = [{'name': item.name, 'expiration_date': item.expiration_date} for item in items]

    return jsonify({"items": items_list}), 200

@main_blueprint.route('/items/expired', methods=['GET'])
def expired_items():
    user_id = request.args.get('user_id')
    today = datetime.now().date()

    items = Item.query.filter(Item.user_id == user_id, Item.expiration_date < today).all()
    items_list = [{'name': item.name, 'expiration_date': item.expiration_date} for item in items]

    return jsonify({"items": items_list}), 200