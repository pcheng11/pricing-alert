from functools import wraps
# from src.app import app
from flask import session, url_for, redirect, request


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            # after user login they will go back to original website
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)

    return decorated_function


def requires_admin_permission(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            # after user login they will go back to original website
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in {"pcheng11@illinois.edu"}:#app.config['ADMINS']:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)

    return decorated_function