from flask import (Blueprint, jsonify, request)
from ..models import Company
from .. import db
from ..utils import Response, PageResult, StockNameResult

bp = Blueprint('company-info-trading', __name__, url_prefix='/v1/company')

session = db.session


@bp.route('/info', methods=('POST',))
def get_company_info():
    ts_code = request.json.get('ts_code')
    print("ts_code: ", ts_code)
    company = session.query(Company).filter_by(ts_code=ts_code).first()
    if company:
        response = Response(200, "get company info success", company, "success")
    else:
        response = Response("fail", "get no company info")
    return jsonify(response.as_dict())
