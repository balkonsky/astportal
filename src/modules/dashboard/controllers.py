from flask import render_template
from flask import Blueprint, current_app, jsonify, abort, g
from flask_security import login_required

import datetime

blueprint = Blueprint('dashboard', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET'])
@login_required
def index():
    current_app.logger.info('get index.html_old page')
    today = datetime.datetime.today().year
    return render_template('index.html', today=today)