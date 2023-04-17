from datetime import datetime
from flask import (Blueprint, jsonify, request)
from flask import session as flask_session
from sqlalchemy.exc import SQLAlchemyError
from ..models import User, Account
from .. import db
from ..utils import Response, PageResult, TokenResult, UserInfoResult

bp = Blueprint('user-management', __name__, url_prefix='/v1/user')

session = db.session


@bp.route('/list', methods=('POST',))
def get_user():
    page = request.json.get('page')
    pageSize = request.json.get('pageSize')
    name = request.json.get('name')
    phone = request.json.get('phone')
    status = request.json.get('status')
    sex = request.json.get('sex')
    query = session.query(User)
    if name:
        query = query.filter_by(name=name)
    if phone:
        query = query.filter_by(phone=phone)
    if status:
        query = query.filter_by(status=status)
    if sex:
        query = query.filter_by(sex=sex)
    users = query.paginate(page=page, per_page=pageSize, error_out=False)
    users_dict = [user.as_dict() for user in users]
    if len(users_dict) == 0:
        response = Response("fail", "get no user")
    else:
        result = PageResult(users_dict, page, users.pages, pageSize)
        response = Response(200, "get users success", result, "success")

    return jsonify(response.as_dict())


@bp.route('/edit', methods=('PUT',))
def edit_user():
    user_id = request.json.get('user_id')
    user_to_update = session.query(User).get(user_id)
    user_to_update.name = request.json.get('name')
    user_to_update.sex = request.json.get('sex')
    user_to_update.nick_name = request.json.get('nick_name')
    user_to_update.phone = request.json.get('phone')
    user_to_update.status = request.json.get('status')
    user_to_update.update_time = datetime.now()
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response = Response("fail", "edit user fail")
    else:
        response = Response("200", "edit user success")
    finally:
        session.close()
    return jsonify(response.as_dict())


@bp.route('/update', methods=('POST',))
def update_user():
    user_id = flask_session.get('user_id')
    user_to_update = session.query(User).get(user_id)
    user_to_update.name = request.json.get('name')
    user_to_update.nick_name = request.json.get('nick_name')
    user_to_update.phone = request.json.get('phone')
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response = Response("fail", "edit user fail")
    else:
        response = Response("200", "edit user success")
    finally:
        session.close()
    return jsonify(response.as_dict())


@bp.route('/delete', methods=('DELETE',))
def delete_user():
    user_id = request.json.get('user_id')

    # 删除user
    user = session.query(User).filter_by(user_id=user_id).first()
    session.delete(user)

    # 删除account
    account = session.query(Account).filter_by(account_id=user.account_id).first()
    session.delete(account)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response = Response("fail", "delete user fail")
    else:
        response = Response("200", "delete user success")
    finally:
        session.close()
    return jsonify(response.as_dict())


@bp.route('/add', methods=('POST',))
def add_user():
    # 为该用户初始化一个账户
    account = Account()
    account.asset = 20000
    account.market_value = 0
    account.money_rest = 20000
    session.add(account)
    session.commit()

    # 获得此前创建的account_id
    account_id = account.account_id
    user = User()
    user.name = request.json.get('name')
    user.nick_name = request.json.get('nick_name')
    user.phone = request.json.get('phone')
    user.sex = request.json.get('sex')
    user.role = request.json.get('role')
    user.status = '启用'
    user.create_time = datetime.now()
    user.update_time = datetime.now()
    user.password = "123456"
    user.account_id = account_id
    session.add(user)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response = Response("fail", "add user fail")
    else:
        response = Response("success", "add user success")
    finally:
        session.close()
    return jsonify(response.as_dict())


@bp.route('/login', methods=('POST',))
def login():
    name = request.json.get('name')
    password = request.json.get('password')
    user = session.query(User).filter_by(name=name).first()
    if user is None:
        response = Response("fail", "user not exist")
    elif user.password != password:
        response = Response("fail", "password error")
    else:
        flask_session['user_id'] = user.user_id
        flask_session['name'] = user.name
        flask_session['role'] = user.role
        flask_session['account_id'] = user.account_id
        tokenResult = TokenResult(" i am token")
        response = Response(200, "login success", tokenResult, "success")
    return jsonify(response.as_dict())


@bp.route('/info', methods=('GET',))
def get_user_info():
    user_id = flask_session.get('user_id')
    user = session.query(User).filter_by(user_id=user_id).first()
    # 向不同的用户分配不同的权限
    admin_permissions = [
        {
            'label': '管理',
            'value': 'manage',
        },
        {
            'label': '用户管理',
            'value': 'user-manage',
        }]
    user_permissions = [{
        'label': '工作台',
        'value': 'dashboard_workplace',
    }]
    if user.role == 'user':
        response = Response(200, "get user info success", UserInfoResult(user, user_permissions), "success")
    else:
        response = Response(200, "get admin info success", UserInfoResult(user, admin_permissions), "success")

    return jsonify(response.as_dict())


@bp.route('/register', methods=('POST',))
def register_user():
    account = Account()
    account.asset = 20000
    account.market_value = 0
    account.money_rest = 20000
    session.add(account)
    session.commit()

    # 获得此前创建的account_id
    account_id = account.account_id
    user = User()
    user.name = request.json.get('name')
    user.nick_name = request.json.get('nick_name')
    user.phone = request.json.get('phone')
    user.sex = request.json.get('sex')
    user.password = request.json.get('password')
    user.role = 'user'
    user.status = '启用'
    user.create_time = datetime.now()
    user.update_time = datetime.now()
    user.account_id = account_id
    session.add(user)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response = Response("fail", "add user fail")
    else:
        response = Response("200", "add user success")
    finally:
        session.close()
    return jsonify(response.as_dict())
