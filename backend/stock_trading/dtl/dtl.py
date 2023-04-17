from datetime import datetime
from flask import (Blueprint, jsonify, request)
from ..models import Dtl
from .. import db
from ..utils import Response, PageResult
from ..utils.util import get_dtl_data

bp = Blueprint('dtl-info', __name__, url_prefix='/v1/dtl')

session = db.session


@bp.route('/list', methods=('POST',))
def get_stock_info():
    page = request.json.get('page')
    pageSize = request.json.get('pageSize')
    ts_code = request.json.get('ts_code')
    name = request.json.get('name')
    trade_date = request.json.get('trade_date')
    get_dtl_data(trade_date=datetime.fromtimestamp(trade_date/1000).strftime('%Y%m%d'))
    query = session.query(Dtl)
    if ts_code:
        query = query.filter_by(ts_code=ts_code)
    if name:
        query = query.filter_by(name=name)
    if trade_date:
        query = query.filter_by(trade_date=datetime.fromtimestamp(trade_date/1000).strftime('%Y%m%d'))

    dtls = query.paginate(page=page, per_page=pageSize, error_out=False)
    dtls_dict = [dtl.as_dict() for dtl in dtls]
    if len(dtls_dict) == 0:
        response = Response("fail", "get no dtl")
    else:
        result = PageResult(dtls_dict, page, dtls.pages, pageSize)
        response = Response(200, "get dtls success", result, "success")

    return jsonify(response.as_dict())
