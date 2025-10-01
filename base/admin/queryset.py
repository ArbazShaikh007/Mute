from base.api.user.models import User, Mind, Session, Feedback
from base.admin.models import Admin, Exercise
from base.database.db import db

def total_user_count():
    return len(User.query.all())



def insert_data(x):
    db.session.add(x)
    db.session.commit()


def all_users():
    return User.query.all()

def mind_count():
    return len(Mind.query.all())


def get_user(email):
    return Admin.query.filter_by(email=email).first()

def get_user_by_id(id):
    return Admin.query.filter_by(id=id).first()

def delete_record(x):
    db.session.delete(x)
    db.session.commit()

def save():
    db.session.commit()

def total_session():
    return len(Session.query.all())


def total_feedback():
    return len(Feedback.query.all())


def total_review_category():
    return len(Mind.query.all())