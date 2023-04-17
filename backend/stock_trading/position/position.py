import datetime
from flask import (Blueprint, jsonify, request)
from sqlalchemy.exc import SQLAlchemyError
from ..models import Position, Account, Order
from .. import db
from ..utils.util import get_order_code, get_market
from ..utils import Response, PageResult, PositionResult
from flask import session as flask_session

bp = Blueprint('stock-position', __name__, url_prefix='/v1/position')

session = db.session


@bp.route('/list', methods=('POST',))
def get_position_info():
    page = request.json.get('page')
    pageSize = request.json.get('pageSize')
    ts_code = request.json.get('ts_code')
    account_id = flask_session.get('account_id')
    query = session.query(Position).filter_by(account_id=account_id)

    if ts_code:
        query = query.filter_by(ts_code=ts_code)

    positions = query.paginate(page=page, per_page=pageSize, error_out=False)
    positions_dict = [position.as_dict() for position in positions]
    if len(positions_dict) == 0:
        response = Response("fail", "get no position")
    else:
        result = PageResult(positions_dict, page, positions.pages, pageSize)
        response = Response(200, "get position success", result, "success")

    return jsonify(response.as_dict())


@bp.route('/buy', methods=('POST',))
def buy_stock():
    ts_code = request.json.get('ts_code')
    if '.' not in ts_code:
        market = get_market(ts_code)
        ts_code = ts_code + "." + market
    market_price = float(request.json.get('market_price'))
    number = float(request.json.get('buy_number'))
    account_id = flask_session.get('account_id')

    # 增加持仓
    position = session.query(Position).filter_by(ts_code=ts_code).first()
    if position:
        position.deal_price = (position.deal_price * position.number + market_price * number) / (
                position.number + number)
        position.number = position.number + number
        position.cost = position.cost + market_price * number
        position.market_price = market_price
        position.market_value = position.market_value + market_price * number
        position.profit_loss = position.market_value - position.cost
        position.deal_time = datetime.datetime.now()
    else:
        deal_price = market_price
        cost = deal_price * number
        market_value = cost
        profit_loss = 0
        deal_time = datetime.datetime.now()
        position = Position(account_id=account_id, ts_code=ts_code, deal_price=deal_price, number=number, cost=cost,
                            market_price=market_price, market_value=market_value, profit_loss=profit_loss,
                            deal_time=deal_time)
        session.add(position)

    # 账户余额和市值变化
    account = session.query(Account).filter_by(account_id=account_id).first()
    account.money_rest = account.money_rest - market_price * number
    account.market_value = account.market_value + market_price * number
    account.asset = account.money_rest + account.market_value

    # 订单记录增加
    order_no = get_order_code()
    user_id = flask_session.get('user_id')
    deal_price = market_price
    deal_number = number
    deal_value = deal_price * deal_number
    deal_date = datetime.datetime.now()
    order = Order(order_no=order_no, user_id=user_id, ts_code=ts_code, type="buy", deal_price=deal_price,
                  deal_number=deal_number, deal_value=deal_value, deal_date=deal_date, status="finished")
    session.add(order)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response = Response("fail", "buy stock fail")
    else:
        response = Response("200", "buy stock success")
    finally:
        session.close()
    return jsonify(response.as_dict())


@bp.route('/sell', methods=('POST',))
def sell_stock():
    ts_code = request.json.get('ts_code')
    market_price = float(request.json.get('market_price'))
    sell_number = float(request.json.get('sell_number'))
    position = session.query(Position).filter_by(ts_code=ts_code).first()
    if position.number < sell_number:
        response = Response("fail", "sell number is more than position number")
        return jsonify(response.as_dict())
    elif position.number == sell_number:
        session.delete(position)
    else:
        position.number = position.number - sell_number
        position.market_price = market_price
        position.cost = position.cost - sell_number * market_price
        position.market_value = position.market_value - sell_number * market_price
        position.deal_time = datetime.datetime.now()

    # 账户余额和市值变化
    account_id = flask_session.get('account_id')
    account = session.query(Account).filter_by(account_id=account_id).first()
    account.money_rest = account.money_rest + sell_number * market_price
    account.market_value = account.market_value - sell_number * market_price
    account.asset = account.money_rest + account.market_value

    # 订单记录增加
    order_no = get_order_code()
    user_id = flask_session.get('user_id')
    deal_price = market_price
    deal_number = sell_number
    deal_value = deal_price * deal_number
    deal_date = datetime.datetime.now()
    order = Order(order_no=order_no, user_id=user_id, ts_code=ts_code, type="sell", deal_price=deal_price,
                  deal_number=deal_number, deal_value=deal_value, deal_date=deal_date, status="finished")
    session.add(order)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response = Response("fail", "sell stock fail")
    else:
        response = Response("200", "sell stock success")
    finally:
        session.close()
    return jsonify(response.as_dict())


@bp.route('/all', methods=('POST',))
def get_position_all():
    account_id = flask_session.get('account_id')
    positions = session.query(Position).filter_by(account_id=account_id).all()
    count = len(positions)
    market_value = sum([p.market_value for p in positions])
    profit_loss = sum([p.profit_loss for p in positions])
    result = PositionResult(count, market_value, profit_loss)
    response = Response(200, "get position success", result, "success")

    return jsonify(response.as_dict())
