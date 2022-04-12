"""Belinsky database worker."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# pylint: disable=E1101
def get_instance(model, **kwargs):
    """Get instance using model query."""
    instance = model.query.filter_by(**kwargs).first()
    return instance


# pylint: disable=no-member
def get_all(model):
    """Get all instances of a model."""
    instances = model.query.all()
    return instances


# pylint: disable=no-member
def add_instance(model, instance_func=None, **kwargs):
    """Add an instance to the database."""
    instance = model(**kwargs)
    if instance_func:
        instance_func(instance)
    db.session.add(instance)
    commit_changes()
    return instance


# pylint: disable=no-member
def delete_instance(model, **kwargs):
    """Delete an instance from the database."""
    db.session.delete(get_instance(model, **kwargs))
    commit_changes()


# pylint: disable=no-member
def edit_instance(model, query_filter, **kwargs):
    """Edit instance attributes in database"""
    instance = get_instance(model, **query_filter)
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()
    return instance


# pylint: disable=no-member
def commit_changes():
    """Commit changes to database."""
    db.session.commit()
