"""Belinsky database worker."""
from typing import Any, Callable

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# pylint: disable=no-member
def get_instance(model: SQLAlchemy, **kwargs) -> SQLAlchemy:
    """Get instance using model query."""
    instance = model.query.filter_by(**kwargs).first()
    return instance


# pylint: disable=no-member
def get_all(model: SQLAlchemy) -> SQLAlchemy:
    """Get all instances of a model."""
    instances = model.query.all()
    return instances


# pylint: disable=no-member
def add_instance(
    model: SQLAlchemy, instance_func: Callable[[SQLAlchemy], None] = None, **kwargs
) -> SQLAlchemy:
    """Add an instance to the database."""
    instance = model(**kwargs)
    if instance_func:
        instance_func(instance)
    db.session.add(instance)
    commit_changes()
    return instance


# pylint: disable=no-member
def delete_instance(model: SQLAlchemy, **kwargs) -> None:
    """Delete an instance from the database."""
    db.session.delete(get_instance(model, **kwargs))
    commit_changes()


# pylint: disable=no-member
def edit_instance(
    model: SQLAlchemy, query_filter: dict[str, Any], **kwargs
) -> SQLAlchemy:
    """Edit instance attributes in database"""
    instance = get_instance(model, **query_filter)
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()
    return instance


# pylint: disable=no-member
def commit_changes() -> None:
    """Commit changes to database."""
    db.session.commit()
