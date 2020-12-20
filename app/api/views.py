# app/auth/views.py

from flask import request, jsonify, current_app, render_template
from functools import wraps
from flask_login import login_required

from . import api
from .. import db
from ..models import ApiKey, Alias, generate_secret, User
from datetime import datetime

import string


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'token' not in request.args:
            return jsonify({"error": "Unauthorized, no token provided"}), 401

        token = request.args.get('token')

        apikeys = ApiKey.query.all()

        for apikey in apikeys:
            if apikey.verify_key(token):
                apikey.last_used = datetime.utcnow()
                db.session.commit()
                return f(apikey.name, apikey.user_id, *args, **kwargs)

        return jsonify({"error": "Unauthorized, token not found"}), 401

    return decorator


@api.route('/api/generate_alias', methods=['GET'])
@token_required
def api_generate(name, user_id):
    """
    Generate Alias from API
    :param name:
    :param user_id:
    :return:
    """

    domain = current_app.config['DOMAIN']
    if domain is None:
        raise Exception("Domain not found")

    source = f'{generate_secret(10, string.ascii_lowercase)}@{domain}'
    destination = User.query.get(user_id).email

    if request.args.get('name'):
        name = request.args.get('name')

    alias_obj = Alias(name=name, source=source, destination=destination, user_id=user_id)

    # add alias to the db
    db.session.add(alias_obj)
    db.session.commit()

    return jsonify({"success": "Successfully generated alias", "alias": source})


@api.route('/api_doc', methods=['GET'])
@login_required
def api_doc():
    """
    API Doc
    :return:
    """

    return render_template('api/api_doc.html', title='API Doc')
