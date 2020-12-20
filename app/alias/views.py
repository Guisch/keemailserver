# app/auth/views.py

import os
from flask import flash, redirect, render_template, url_for, current_app
from flask_login import login_required, current_user

from . import alias
from .forms import NewAliasForm
from .. import db
from ..models import Alias, generate_secret
import string


@alias.route('/aliases/add', methods=['GET', 'POST'])
@login_required
def aliases_add():
    """
    Handle requests to /aliases/add route
    New Alias
    :return:
    """

    domain = current_app.config['DOMAIN']
    if domain is None:
        raise Exception("Domain not found")

    default_source = f'{generate_secret(10, string.ascii_lowercase)}@{domain}'
    form = NewAliasForm(source=default_source, destination=current_user.email)

    if form.validate_on_submit():
        alias_obj = Alias(name=form.name.data, source=form.source.data,
                          destination=form.destination.data, user_id=current_user.id)

        # add alias to the db
        db.session.add(alias_obj)
        db.session.commit()
        flash('Successfully added new alias')

        # redirect to page
        return redirect(url_for('alias.aliases'))

    return render_template('alias/aliases_add.html', form=form, title='New Alias')


@alias.route('/aliases', methods=['GET', 'POST'])
@login_required
def aliases():
    """
    Handle requests to /aliases route
    List user aliases
    :return:
    """

    aliases_list = Alias.query.filter_by(user_id=current_user.id).all()

    return render_template('alias/aliases.html', aliases=aliases_list, title='Aliases')


@alias.route('/aliases/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def aliases_del(id):
    """
    Handle requests to /aliases/delete/<id> route
    Delete Alias
    :return:
    """

    aliases_list = Alias.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(aliases_list)
    db.session.commit()
    flash('Successfully deleted Alias')

    return redirect(url_for('alias.aliases'))
