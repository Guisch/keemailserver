# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from . import apikey
from .forms import GenerateApiKeyForm
from .. import db
from ..models import ApiKey


@apikey.route('/apikeys/add', methods=['GET', 'POST'])
@login_required
def apikeys_add():
    """
    Handle requests to /apikeys/add route
    Generate an API Key
    :return:
    """

    form = GenerateApiKeyForm()
    if form.validate_on_submit():
        api_key = ApiKey(name=form.name.data, user_id=current_user.id)
        key = api_key.key

        # add key to the db
        db.session.add(api_key)
        db.session.commit()
        flash('API Key successfully generated')
        flash('Save it ! You won\'t be able to recover it', 'warning')
        flash(f'Key: {key}')

        # redirect to page
        return redirect(url_for('apikey.apikeys'))

    return render_template('apikey/apikeys_add.html', form=form, title='Generate API Key')


@apikey.route('/apikeys', methods=['GET', 'POST'])
@login_required
def apikeys():
    """
    Handle requests to /apikeys route
    List API Keys
    :return:
    """

    apikeys_list = ApiKey.query.filter_by(user_id=current_user.id).all()

    return render_template('apikey/apikeys.html', apikeys=apikeys_list, title='API Keys')


@apikey.route('/apikeys/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def apikeys_del(id):
    """
    Handle requests to /apikeys/delete/<id> route
    Delete API Keys
    :return:
    """

    apikey_obj = ApiKey.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(apikey_obj)
    db.session.commit()
    flash('Successfully deleted API Key')

    return redirect(url_for('apikey.apikeys'))
