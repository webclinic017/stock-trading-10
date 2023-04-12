from flask import (Blueprint, jsonify, request)
from ..models import Order
from .. import db
from flask import session as flask_session
from ..utils import Response, OrderResult

bp = Blueprint('order-info', __name__, url_prefix='/v1/order')

session = db.session


@bp.route('/list', methods=('POST',))
def get_order_info():
    page = request.json.get('page')
    pageSize = request.json.get('pageSize')
    order_no = request.json.get('order_no')
    type = request.json.get('type')
    status = request.json.get('status')
    user_id = flask_session.get('user_id')
    query = session.query(Order).filter_by(user_id=user_id)

    if order_no:
        query = query.filter_by(order_no=order_no)
    if type:
        query = query.filter_by(type=type)
    if status:
        query = query.filter_by(status=status)
    orders = query.paginate(page=page, per_page=pageSize, error_out=False)
    orders_dict = [stock.as_dict() for stock in orders]
    if len(orders_dict) == 0:
        response = Response("fail", "get no order")
    else:
        result = PageResult(orders_dict, page, orders.pages, pageSize)
        response = Response(200, "get orders success", result, "success")

    return jsonify(response.as_dict())


@bp.route('/all', methods=('POST',))
def get_order_all():
    user_id = flask_session.get('user_id')
    orders = session.query(Order).filter_by(user_id=user_id).all()
    buy_orders = session.query(Order).filter_by(user_id=user_id, type='buy').all()
    count = len(orders)
    deal_value = sum([o.deal_value for o in orders])
    buy_count = len(buy_orders)
    result = OrderResult(count, deal_value, buy_count)
    response = Response(200, "get orders success", result, "success")
    return jsonify(response.as_dict())
