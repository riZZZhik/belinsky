from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_instance(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    return instance


def get_all(model):
    instances = model.query.all()
    return instances


def add_instance(model, instance_func=None, **kwargs):
    instance = model(**kwargs)
    if instance_func:
        instance_func(instance)
    db.session.add(instance)
    commit_changes()
    return instance


def delete_instance(model, **kwargs):
    db.session.delete(get_instance(model, **kwargs))
    commit_changes()


def edit_instance(model, query_filter, **kwargs):
    instance = get_instance(model, **query_filter)
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()
    return instance


def commit_changes():
    db.session.commit()
