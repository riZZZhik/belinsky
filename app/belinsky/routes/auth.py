"""Belinsky authentication blueprint."""
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from prometheus_client import Summary
from werkzeug import Response

from .utils import check_request_keys
from .. import database, models

# Initialize login manager
login_manager = LoginManager()

# Initialize prometheus metrics
SIGNUP_LATENCY = Summary("signup_latency", 'Latency of "signup" request')
LOGIN_LATENCY = Summary("login_latency", 'Latency of "login" request')
LOGOUT_LATENCY = Summary("logout_latency", 'Latency of "logout" request')
DELETE_USER_LATENCY = Summary("delete_user_latency", 'Latency of "delete-user" request')


@SIGNUP_LATENCY.time()
def signup() -> Response | str | tuple[dict[str, str | int], int]:
    """Sign up"""

    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # Return template if request.method is GET
    if request.method == "GET":
        return render_template("signup.html")

    # Check if user with given username already exists
    user = database.get_instance(models.User, username=request.form.get("username"))
    if user:
        flash(f"User with {request.form.get('username')} username already exists.")
        return redirect(url_for("auth.signup"))

    # Add user to database
    user = database.add_instance(
        models.User,
        lambda i: i.set_password(request.form.get("password")),
        username=request.form.get("username"),
    )
    login_user(user, remember=True)

    if request.form.get("raw"):
        response = {
            "info": f'Successfully signed up as {request.form.get("username")}.',
            "status": 200,
        }
        return response, 200

    return redirect(url_for("home"))


@LOGIN_LATENCY.time()
def login() -> Response | str | tuple[dict[str, str | int], int]:
    """Login"""

    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # Return template if request.method is GET
    if request.method == "GET":
        return render_template("login.html")

    # Check if user exists and password correct
    user = database.get_instance(models.User, username=request.form.get("username"))
    if not user:
        flash(f"User with {request.form.get('username')} username not found.")
        return redirect(url_for("auth.login"))

    if not user.check_password(request.form.get("password")):
        flash("Invalid password. Please try again.")
        return redirect(url_for("auth.login"))

    # Login user
    login_user(user, remember=request.form.get("remember") == "on")

    if request.form.get("raw"):
        response = {
            "info": f'Successfully logged in as {request.form.get("username")}.',
            "status": 200,
        }
        return response, 200

    return redirect(url_for("home"))


@LOGOUT_LATENCY.time()
def logout() -> tuple[dict[str, str | int], int] | Response:
    """Logout"""

    # Bypass if user is logged in
    if current_user.is_authenticated:
        logout_user()

    if request.form.get("raw"):
        response = {"info": "Successfully logged out.", "status": 200}
        return response, 200

    return redirect(url_for("home"))


@DELETE_USER_LATENCY.time()
def delete_user() -> tuple[dict[str, str | int], int]:
    """Delete user.
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
    required_keys = {"username", "password"}
    check = check_request_keys(required_keys)
    if check:
        return check

    # Check if user exists and password correct
    user = database.get_instance(models.User, username=request.json["username"])
    if not user:
        response = {
            "error": f"User with {request.json['username']} username not found.",
            "status": 406,
        }
        return response, 406

    if not user.check_password(request.json["password"]):
        response = {"error": "Invalid password. Please try again.", "status": 406}
        return response, 406

    # Logout if it is current user
    if (
        current_user.is_authenticated
        and current_user.username == request.json["username"]
    ):
        logout_user()

    # Delete user
    database.delete_instance(models.User, username=request.json["username"])

    response = {
        "result": f"Successfully deleted {request.json['username']} user.",
        "status": 200,
    }
    return response, 200


@login_manager.user_loader
def load_user(user_id) -> database.db or None:
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return database.get_instance(models.User, id=user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized_handler() -> tuple[dict[str, str | int], int] | Response:
    """401 Unauthorized handler."""
    if request.form.get("raw"):
        response = {"error": "Unauthorized. Please login first.", "status": 401}
        return response, 401

    return redirect(url_for("home"))


def create_blueprint_auth() -> Blueprint:
    """Create authentication blueprint."""
    auth_bp = Blueprint("auth", __name__, template_folder="../templates")

    auth_bp.add_url_rule("/signup", view_func=signup, methods=["GET", "POST"])
    auth_bp.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
    auth_bp.add_url_rule("/logout", view_func=logout, methods=["GET", "POST"])
    auth_bp.add_url_rule("/delete-user", view_func=delete_user, methods=["GET", "POST"])

    return auth_bp
