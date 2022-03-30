from flask import Blueprint, request
from flask_login import LoginManager, current_user, login_user, logout_user

from ..database import add_instance, get_instance, delete_instance
from ..models import User

login_manager = LoginManager()


def signup():
    """ Sign up.
    ---
    Body (JSON):
        - username: Username.
        - password: Password.

    Responses:
        200:
            description: Return that request processed properly.
            schema:
                result: 'Successfully signed up'
                status: 200
        400:
            description: Json body or 'username', 'password' keys not found in request body.
            schema:
                error: Error description.
                status: 400
        406:
            description: User with given username already exists.
            schema:
                error: Error description.
                status: 406
    """

    # Check input body
    if not request.json:
        response = {
            'error': "Json body not found in request.",
            'status': 400
        }
        return response, 400

    required_keys = ['username', 'password']
    if not all([key in required_keys for key in request.json.keys()]):
        response = {
            'error': 'Not enough keys in request. Required keys: %s.' % ", ".join(required_keys),
            'status': 400
        }
        return response, 400

    # Check if user with given username already exists
    user = get_instance(User, username=request.json['username'])
    if user:
        response = {
            'error': 'User with %s username already exists.' % request.json['username'],
            'status': 406
        }
        return response, 406

    # Add user to database
    instance_func = lambda instance: instance.set_password(request.json['password'])
    user = add_instance(User, instance_func, username=request.json['username'])
    login_user(user, remember=True)

    response = {
        'result': 'Successfully signed up as %s.' % user.username,
        'status': 200
    }
    return response, 200


def login():
    """ Login.
    ---
    Body (JSON):
        - username: Username.
        - password: Password.

    Responses:
        200:
            description: Return that request processed properly.
            schema:
                result: 'Successfully logged in'
                status: 200
        400:
            description: Json body or ['username', 'password'] keys not found in request body.
            schema:
                error: Error description.
                status: 400
        406:
            description: User with given username not found OR Invalid password.
            schema:
                error: Error description.
                status: 406
    """

    # Bypass if user is logged in
    if current_user.is_authenticated:
        response = {
            'result': 'Already logged in as %s.' % current_user.username,
            'status': 200
        }
        return response, 200

    # Check input body
    if not request.json:
        response = {
            'error': "Json body not found in request.",
            'status': 400
        }
        return response, 400

    required_keys = ['username', 'password']
    if not all([key in required_keys for key in request.json.keys()]):
        response = {
            'error': 'Not enough keys in request. Required keys: %s.' % ", ".join(required_keys),
            'status': 400
        }
        return response, 400

    # Check if user exists and password correct
    user = get_instance(User, username=request.json['username'])
    if not user:
        response = {
            'error': 'User with %s username not found. Please signup first.' % request.json['username'],
            'status': 406
        }
        return response, 406

    if not user.check_password(request.json['password']):
        response = {
            'error': 'Invalid password. Please try again.',
            'status': 406
        }
        return response, 406

    # Login user
    login_user(user, remember=True)
    response = {
        'result': 'Successfully logged in as %s.' % user.username,
        'status': 200
    }
    return response, 200


def logout():
    """ Logout.
    ---
    Responses:
        200:
            description: Return that request processed properly.
            schema:
                result: 'Successfully logged out.'
                status: 200
        406:
            description: User are not logged in.
            schema:
                error: You are not logged in.
                status: 406
    """

    if not current_user.is_authenticated:
        response = {
            'error': 'You are not logged in.',
            'status': 406
        }
        return response, 406

    logout_user()
    response = {
        'result': 'Successfully logged out.',
        'status': 200
    }
    return response, 200


def delete_user():
    """ Delete user.
    ---
    Body (JSON):
        - username: Username.
        - password: Password.

    Responses:
        200:
            description: Return that request processed properly.
            schema:
                result: 'Successfully deleted user.'
                status: 200
        400:
            description: Json body or ['username', 'password'] keys not found in request body.
            schema:
                error: Error description.
                status: 400
        406:
            description: User with given username not found OR Invalid password.
            schema:
                error: Error description.
                status: 406
    """

    # Check input body
    if not request.json:
        response = {
            'error': "Json body not found in request.",
            'status': 400
        }
        return response, 400

    required_keys = ['username', 'password']
    if not all([key in required_keys for key in request.json.keys()]):
        response = {
            'error': 'Not enough keys in request. Required keys: %s.' % ", ".join(required_keys),
            'status': 400
        }
        return response, 400

    # Check if user exists and password correct
    user = get_instance(User, username=request.json['username'])
    if not user:
        response = {
            'error': 'User with %s username not found.' % request.json['username'],
            'status': 406
        }
        return response, 406

    if not user.check_password(request.json['password']):
        response = {
            'error': 'Invalid password. Please try again.',
            'status': 406
        }
        return response, 406

    # Logout if it is current user
    if current_user.is_authenticated and current_user.username == request.json['username']:
        logout_user()

    # Delete user
    delete_instance(User, username=request.json['username'])

    response = {
        'result': "Successfully deleted %s user." % request.json['username'],
        'status': 200
    }
    return response, 200


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return get_instance(User, id=user_id)
    return None


def create_blueprint_auth():
    auth_bp = Blueprint('auth_bp', __name__)

    auth_bp.add_url_rule('/signup', view_func=signup, methods=['GET', 'POST'])
    auth_bp.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
    auth_bp.add_url_rule('/logout', view_func=logout, methods=['GET', 'POST'])
    auth_bp.add_url_rule('/delete-user', view_func=delete_user, methods=['GET', 'POST'])

    return auth_bp