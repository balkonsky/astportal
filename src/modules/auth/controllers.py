from flask import Blueprint, current_app, jsonify, abort, g
from flask_jwt_extended import current_user, jwt_required, create_access_token

from backend.src.utils import validation_required, json_required, active_directory
from .schema import login_schema
from backend.src.models import User
from backend.src import db, log


blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/auth', methods=['POST'])
@json_required
@validation_required(login_schema)
def login():
    ad = active_directory.AD(
        host='172.20.2.67',
        port=389,
        username='dev-chat-svc',
        password='4gSn3dhU18',
        basedn='OU=Accounts,DC=corp,DC=humans,DC=net',
        domain='',
        ssl=False,
        timeout=20)
    username = g.body['login'].lower()
    if not ad.check_auth('\\' + username, g.body['password']):
        current_app.logger.warning(f'User {username} login failed')
        abort(401, 'Invalid credentials')

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
    profile = ad.get_user_profile(username)
    current_app.logger.debug(f'Login profile: {profile}')
    db.session.add(user)
    db.session.commit()

    current_app.logger.info(f'User {username} login success')

    return jsonify(token=create_access_token(user.id))


