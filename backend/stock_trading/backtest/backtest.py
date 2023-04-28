from flask import (Blueprint, jsonify, request)
from .. import db
from ..quotation.quotation import date_deal
from ..utils import Response, BackTestResult
from ..utils.backtest_from_tushare import backtest

bp = Blueprint('backtest', __name__, url_prefix='/v1/backtest')

session = db.session


@bp.route('/info', methods=('POST',))
def get_backtest_info():
    ts_code = request.json.get('ts_code')
    cash = float(request.json.get('cash'))
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_date, end_date = date_deal(start_date, end_date)
    end_cash = backtest(ts_code, start_date, end_date, cash)

    result = BackTestResult(end_cash)
    if end_cash:
        response = Response(200, "back test success", result, "success")
    else:
        response = Response("fail", "back test fail")
    return jsonify(response.as_dict())
