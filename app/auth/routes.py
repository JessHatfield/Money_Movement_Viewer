from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        current_app.logger.info(f"{current_user} Has Logged In")
        return redirect(url_for('money_movement.view_all_money_movements'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()

        # If user does not exist or password is invalid then reject login
        if user is None or not user.check_password(form.password.data):
            current_app.logger.info(f'Could Find Not User For Email {form.username.data}')
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

        # If password is valid and user exists then log the user in
        login_user(user, remember=form.remember_me.data)
        current_app.logger.info(f"{current_user} Has Logged In")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('money_movement.view_all_money_movements')
        return redirect(next_page)

    return render_template('auth/login.html', title=('Sign In'), form=form)


@bp.route('/logout')
def logout():
    current_user_id = current_user.id

    logout_user()
    current_app.logger.info(f"<User {current_user_id}> Has Logged Out")

    return redirect(url_for('money_movement.view_all_money_movements'))
