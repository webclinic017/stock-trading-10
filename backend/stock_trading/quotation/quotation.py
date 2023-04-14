from datetime import datetime
from flask import (Blueprint, jsonify, request)
from backend.stock_trading.utils import Response, RealTimeResult
import tushare as ts
from backend.stock_trading.config import TOKEN
from .. import db
from ..models import Stock

bp = Blueprint('quotation-data', __name__, url_prefix='/v1/quotation')

pro = ts.pro_api(TOKEN)
session = db.session


@bp.route('/daily', methods=('POST',))
def get_daily_info():
    ts_code, start_date, end_date = get_front_params()
    if ts_code is None and start_date is None and end_date is None:
        response = Response(404, "股票名称和TS代码不一致")
        return jsonify(response.as_dict())

    # Request daily Interface of Tushare Pro to get daily-k-line
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    trade_date_list = df['trade_date'].tolist()
    data_list = df[['open', 'close', 'low', 'high']].values.tolist()
    trade_date_list.reverse()
    data_list.reverse()
    if len(data_list) == 0:
        response = Response("fail", "get no daily-k-line")
    else:
        result = RealTimeResult(trade_date_list, data_list)
        response = Response(200, "get daily-k-line success", result, "success")
    return jsonify(response.as_dict())


@bp.route('/weekly', methods=('POST',))
def get_weekly_info():
    ts_code, start_date, end_date = get_front_params()
    if ts_code is None and start_date is None and end_date is None:
        response = Response(404, "股票名称和TS代码不一致")
        return jsonify(response.as_dict())

    # Request weekly Interface of Tushare Pro to get daily-k-line
    df = pro.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
    trade_date_list = df['trade_date'].tolist()
    data_list = df[['open', 'close', 'low', 'high']].values.tolist()
    trade_date_list.reverse()
    data_list.reverse()
    if len(data_list) == 0:
        response = Response("fail", "get no weekly-k-line")
    else:
        result = RealTimeResult(trade_date_list, data_list)
        response = Response(200, "get weekly-k-line success", result, "success")
    return jsonify(response.as_dict())


@bp.route('/monthly', methods=('POST',))
def get_monthly_info():
    ts_code, start_date, end_date = get_front_params()
    if ts_code is None and start_date is None and end_date is None:
        response = Response(404, "股票名称和TS代码不一致")
        return jsonify(response.as_dict())

    # Request monthly Interface of Tushare Pro to get daily-k-line
    df = pro.monthly(ts_code=ts_code, start_date=start_date, end_date=end_date)
    trade_date_list = df['trade_date'].tolist()
    data_list = df[['open', 'close', 'low', 'high']].values.tolist()
    trade_date_list.reverse()
    data_list.reverse()
    if len(data_list) == 0:
        response = Response("fail", "get no monthly-k-line")
    else:
        result = RealTimeResult(trade_date_list, data_list)
        response = Response(200, "get monthly-k-line success", result, "success")
    return jsonify(response.as_dict())


def date_deal(start_date, end_date):
    if start_date:
        start_date = datetime.fromtimestamp(start_date / 1000).strftime('%Y%m%d')
    else:
        start_date = '20210101'
    if end_date:
        end_date = datetime.fromtimestamp(end_date / 1000).strftime('%Y%m%d')
    else:
        end_date = datetime.now().strftime('%Y%m%d')
    return start_date, end_date


def get_front_params():
    ts_code = request.json.get('ts_code')
    name = request.json.get('name')
    stock = session.query(Stock).filter_by(name=name).first()
    if stock:
        # stock和ts_code不一致
        if not (ts_code is None or ts_code == '') and ts_code != stock.ts_code:
            return None, None, None
        else:
            ts_code = stock.ts_code
    if not ts_code:
        ts_code = '000001.SZ'
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = date_deal(start_date, end_date)
    return ts_code, start_date, end_date
