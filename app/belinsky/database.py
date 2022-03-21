from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_instance(model, **kwargs):
    data = model.query.filter_by(**kwargs).first()
    return data


def get_all(model):
    data = model.query.all()
    return data


def add_instance(model, instance_func=None, **kwargs):
    instance = model(**kwargs)
    if instance_func:
        instance_func(instance)
    db.session.add(instance)
    commit_changes()
    return instance


def delete_instance(model, username):
    model.query.filter_by(username=username).delete()
    commit_changes()


def edit_instance(model, query_filter, **kwargs):
    instance = get_instance(model, **query_filter)
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()
    return instance


def commit_changes():
    db.session.commit()
