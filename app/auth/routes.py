from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User
import logging

logger=logging.getLogger(__name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('money_movement.view_all_money_movements'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            logger.debug(f'Could Not Find Entry In DB For {form.username.data}')
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        logger.debug(f'{form.username.data} Has Logged In')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('money_movement.view_all_money_movements')
        return redirect(next_page)
    return render_template('auth/login.html', title=('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('money_movement.view_all_money_movements'))



