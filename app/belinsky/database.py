"""Belinsky database worker."""
# pylint: disable=no-member
import typing as t

from flask_sqlalchemy import SQLAlchemy
from loguru import logger

db = SQLAlchemy()


def get_instance(model: db.Model, **kwargs) -> db.Model:
    """Get instance using model query."""
    instance = model.query.filter_by(**kwargs).first()

    logger.debug(f"Got {instance} instance from database.")
    return instance


def get_all(model: db.Model) -> db.Model:
    """Get all instances of a model."""
    instances = model.query.all()

    logger.debug(f"Got {instances} instances from database.")
    return instances


def add_instance(
    model: db.Model, instance_func: t.Callable[[db.Model], None] = None, **kwargs
) -> db.Model:
    """Add an instance to the database."""
    instance = model(**kwargs)
    if instance_func:
        instance_func(instance)
    db.session.add(instance)
    commit_changes()

    logger.debug(f"Added {instance} instance to database.")
    return instance


def delete_instance(model: db.Model, **kwargs) -> None:
    """Delete an instance from the database."""
    instance = get_instance(model, **kwargs)
    db.session.delete(instance)
    commit_changes()

    logger.debug(f"Deleted {instance} instance from database.")


def edit_instance(
    model: db.Model, query_filter: dict[str, t.Any], **kwargs
) -> db.Model:
    """Edit instance attributes in database"""
    instance = get_instance(model, **query_filter)
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()

    logger.debug(f"Edited {instance} instance in database with {kwargs} attributes.")
    return instance


def commit_changes() -> None:
    """Commit changes to database."""
    db.session.commit()
