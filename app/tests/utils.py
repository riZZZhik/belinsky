"""Belinsky tests utils."""
from contextlib import contextmanager

from flask import Flask, template_rendered

from belinsky import database, models


# Utils to assert rendered template
@contextmanager
def captured_templates(app):
    """Get rendered_template information."""
    recorded = []

    # noinspection PyUnusedLocal
    # pylint: disable=unused-argument
    def record(sender, template, context, **extra):
        """Append template and context to recorded templates."""
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


# Utils to interact with app database
def add_user(_app: Flask, username: str, password: str) -> None:
    """Add user model to database."""
    with _app.app_context():
        if database.get_instance(models.User, username=username) is None:
            database.add_instance(
                models.User,
                lambda instance: instance.set_password(password),
                username=username,
            )


def delete_user(_app: Flask, username: str) -> None:
    """Delete user model from database."""
    with _app.app_context():
        if database.get_instance(models.User, username=username) is not None:
            database.delete_instance(models.User, username=username)
