from flask import session as flask_session
from flask import (Blueprint, jsonify, request)
from ..utils.util import get_market_value
from ..models import Stock, Account
from .. import db
from ..utils import Response, PageResult, StockNameResult
from ..utils.result import MarketPriceResult

bp = Blueprint('stock-info-trading', __name__, url_prefix='/v1/stock')

session = db.session


@bp.route('/list', methods=('POST',))
def get_stock_info():
    page = request.json.get('page')
    pageSize = request.json.get('pageSize')
    ts_code = request.json.get('ts_code')
    name = request.json.get('name')
    market = request.json.get('market')
    query = session.query(Stock)
    if ts_code:
        query = query.filter_by(ts_code=ts_code)
    if name:
        query = query.filter_by(name=name)
    if market:
        query = query.filter_by(market=market)
    stocks = query.paginate(page=page, per_page=pageSize, error_out=False)
    stocks_dict = [stock.as_dict() for stock in stocks]
    if len(stocks_dict) == 0:
        response = Response("fail", "get no stock")
    else:
        result = PageResult(stocks_dict, page, stocks.pages, pageSize)
        response = Response(200, "get stocks success", result, "success")

    return jsonify(response.as_dict())


@bp.route('/market_price', methods=('POST',))
def get_market_price():
    ts_code = request.json.get('ts_code')
    market_price = get_market_value(ts_code)
    account_id = flask_session.get('account_id')
    money_rest = session.query(Account).filter_by(account_id=account_id).first().money_rest
    # TODO 当前不是交易日，是否确实返回0
    if market_price == 0:
        response = Response("fail", "当前不是交易日，请择日购入")
    else:
        market_price_result = MarketPriceResult(market_price, money_rest)
        response = Response(200, "get stocks success", market_price_result, "success")
    return jsonify(response.as_dict())


@bp.route('/stock_names', methods=('POST',))
def get_stock_names():
    stock_names = [row[0] for row in session.query(Stock.name).all()]
    result = StockNameResult(stock_names)
    if len(stock_names) == 0:
        response = Response("fail", "get no stock")
    else:
        response = Response(200, "get stocks success", result, "success")
    return jsonify(response.as_dict())
