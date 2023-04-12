from datetime import datetime
from flask import (Blueprint, jsonify, request)
from backend.stock_trading.utils import Response, RealTimeResult
import tushare as ts
from backend.stock_trading.config import TOKEN

bp = Blueprint('indexQuotation-data', __name__, url_prefix='/v1/indexQuotation')

pro = ts.pro_api(TOKEN)


@bp.route('/index_daily', methods=('POST',))
def get_daily_info():
    ts_code = request.json.get('ts_code', '000001.SH')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = date_deal(start_date, end_date)

    # Request index_daily Interface of Tushare Pro to get daily-k-line
    df = pro.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    trade_date_list = df['trade_date'].tolist()
    data_list = df[['open', 'close', 'low', 'high']].values.tolist()
    trade_date_list.reverse()
    data_list.reverse()
    if len(data_list) == 0:
        response = Response("fail", "get no index_daily-k-line")
    else:
        result = RealTimeResult(trade_date_list, data_list)
        response = Response(200, "get index_daily-k-line success", result, "success")
    return jsonify(response.as_dict())


@bp.route('/index_weekly', methods=('POST',))
def get_weekly_info():
    ts_code = request.json.get('ts_code', '000001.SH')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = date_deal(start_date, end_date)

    # Request index_weekly Interface of Tushare Pro to get daily-k-line
    df = pro.index_weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
    trade_date_list = df['trade_date'].tolist()
    data_list = df[['open', 'close', 'low', 'high']].values.tolist()
    trade_date_list.reverse()
    data_list.reverse()
    if len(data_list) == 0:
        response = Response("fail", "get no index_weekly-k-line")
    else:
        result = RealTimeResult(trade_date_list, data_list)
        response = Response(200, "get index_weekly-k-line success", result, "success")
    return jsonify(response.as_dict())


@bp.route('/index_monthly', methods=('POST',))
def get_monthly_info():
    ts_code = request.json.get('ts_code', '000001.SH')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = date_deal(start_date, end_date)

    # Request index_monthly Interface of Tushare Pro to get daily-k-line
    df = pro.index_monthly(ts_code=ts_code, start_date=start_date, end_date=end_date)
    trade_date_list = df['trade_date'].tolist()
    data_list = df[['open', 'close', 'low', 'high']].values.tolist()
    trade_date_list.reverse()
    data_list.reverse()
    if len(data_list) == 0:
        response = Response("fail", "get no index_monthly-k-line")
    else:
        result = RealTimeResult(trade_date_list, data_list)
        response = Response(200, "get index_monthly-k-line success", result, "success")
    return jsonify(response.as_dict())


def date_deal(start_date, end_date):
    if start_date:
        start_date = datetime.fromtimestamp(start_date / 1000).strftime('%Y%m%d')
    else:
        start_date = '20230101'
    if end_date:
        end_date = datetime.fromtimestamp(end_date / 1000).strftime('%Y%m%d')
    else:
        end_date = datetime.now().strftime('%Y%m%d')
    return start_date, end_date
