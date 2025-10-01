from base import login_manager
import os
from base.database.db import db
from flask_login import UserMixin
from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer as Serializer
from base.common.utils import COMMON_URL

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(150),nullable=True)
    lname=db.Column(db.String(150),nullable=True)
    email=db.Column(db.String(150),unique=True,nullable=True)
    phone=db.Column(db.String(150),nullable=True)
    image_file=db.Column(db.String(150),nullable=True)
    audio_file=db.Column(db.String(150),nullable=True)
    password = db.Column(db.String(150),nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
  

    def get_token(self,expiress_sec=1800):
        serial = Serializer(os.getenv("SECRET_KEY"))
        return serial.dumps({'user_id': self.id})

    @staticmethod
    def verify_admin_token(token, expiress_sec=1800):
        serial = Serializer(os.getenv("SECRET_KEY"))
        try:
            user_id = serial.loads(token, max_age=expiress_sec)['user_id']
        except:
            return None
        return Admin.query.get(user_id)

class Terms(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        content=db.Column(db.Text,nullable=True)
        created_at = db.Column(db.Date)
        updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

        def as_dict(self):
            return{
                'id':self.id,
                'content':self.content
        }

class Privacy(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text,nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def as_dict(self):
        return{
            'id':self.id,
            'content':self.content
        }

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cat_name=db.Column(db.String(150),nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

class Exercise(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=True)
    description=db.Column(db.Text,nullable=True)
    tags=db.Column(db.Text,nullable=True)
    image_file=db.Column(db.String(150),nullable=True)
    audio_file=db.Column(db.String(150),nullable=True)
    likes=db.Column(db.Integer,nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE', onupdate = 'CASCADE'))
    exercise_like_data = db.relationship('MindSubCategorylikes', backref='exercise_like_data')

    def as_dict(self):
        return{
            'id':self.id,
            'title':self.title,
            'description':self.description,
            'tags':self.tags,
            'audio_file': COMMON_URL + "/static/audio/"+ self.audio_file if self.audio_file is not None else "",
            'image_file': COMMON_URL + "/static/exercise_image/"+ self.image_file if self.image_file is not None else '',
            'likes':self.likes if self.likes is not None else 0,
            "post_type": "audio"
        }

# class Body_likes(db.Model):
#         id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#         user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
#         exercise_id=db.Column(db.Integer,db.ForeignKey('exercise.id',ondelete='CASCADE',onupdate='CASCADE'))
#         created_at=db.Column(db.Date)
#         updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow())
#
#         def as_dict(self):
#             return{
#             "id":self.id,
#             "exercise_id":self.exercise_id,
#             "created_at":self.created_at.strftime("%b %d,%Y")
#         }


# class Exercise_mul_image(db.Model):
#      id = db.Column(db.Integer,primary_key=True)
#      title=db.Column(db.String(150),nullable=True)
#      created_at = db.Column(db.Date)
#      updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
#      exercise_id=db.Column(db.Integer,db.ForeignKey('exercise.id',ondelete='CASCADE',onupdate='CASCADE'))

#      def as_dict(self):
#         return{
#            'id':self.id,
#            'title':self.title

#       }