from flask import session as flask_session
from flask import (Blueprint, jsonify)
from ..models import Account
from .. import db
from ..utils import Response, AccountResult

bp = Blueprint('account-info', __name__, url_prefix='/v1/account')

session = db.session


@bp.route('/all', methods=('POST',))
def get_account_info():
    account_id = flask_session.get('account_id')

    account = session.query(Account).filter_by(account_id=account_id).first()
    if account is None:
        response = Response("fail", "get no account")
    else:
        result = AccountResult(account)
        response = Response(200, "get account success", result, "success")

    return jsonify(response.as_dict())
