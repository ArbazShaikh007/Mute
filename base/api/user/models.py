import jwt,os
from base.database.db import db
from datetime import datetime
from werkzeug.security import check_password_hash
from flask import request, jsonify, url_for
from functools import wraps
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer as Serializer
import pytz
from base.admin.models import Exercise
from base.common.utils import COMMON_URL
from dotenv import load_dotenv

load_dotenv('/home/ArbazShaikh007/mysite/mute/base/.env')

class User(db.Model):
    id=db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    fullname=db.Column('fullname',db.String(100))
    username=db.Column('username',db.String(100))
    email=db.Column('email', db.String(100))
    password=db.Column('password', db.String(300))
    birthdate = db.Column('birthdate', db.DateTime)
    discord_link=db.Column('discord_link',db.String(100)) 
    image_name=db.Column('photo_name',db.String(225))
    is_block=db.Column(db.Boolean,default=False)
    contact = db.relationship('Contact_us',backref='user',lazy=True)
    reflect = db.relationship('Reflect', backref='user', lazy=True)
    listen = db.relationship('Listen', backref='user', lazy=True)
    mind_sub_cat = db.relationship('MindSubCategory', backref='user', lazy=True)
    session = db.relationship('Session', backref='user', lazy=True)
    feedback = db.relationship('Feedback', backref='feed', lazy=True)
    device_id=db.Column('device_id', db.String(300))
    social_id=db.Column('social_id', db.String(300))
    device_type=db.Column('device_type', db.String(300))
    social_type=db.Column('social_type', db.String(300))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at=db.Column(db.Date)
    updated_at=db.Column(db.DateTime, onupdate=datetime.utcnow())
    parents_monitoring=db.Column(db.Boolean,default=False)

    def check_password(self, password):
            return check_password_hash(self.password, password)

    def as_dict(self,token):
            return{ 
            'id': self.id,
            'fullname':self.fullname if self.fullname is not None else '',
            'username': self.username,
            'email': self.email,
            'birthdate': self.birthdate,
            'token':token,
            "image_name": COMMON_URL+"/static/profile_pic/"+self.image_name if self.image_name else ""
        }
    
    def login_res(self,token):
            return{ 
            'id': self.id,
            'fullname':self.fullname if self.fullname is not None else '',
            'username': self.username,
            'email': self.email,
            'birthdate': self.birthdate,
            'token':token,
            "image_name": COMMON_URL+"/static/profile_pic/"+self.image_name if self.image_name else ""
        }    

    def user_data(self,token = ''):
            return{ 
            'id': self.id,
            'fullname': self.fullname if self.fullname is not None else '',
            'username': self.username,
            'email': self.email,
            'birthdate': self.birthdate,
            'token':token,
            "image_name": COMMON_URL+"/static/profile_pic/"+self.image_name if self.image_name else ""
        }

    def get_token(self,expire_sec=1800):
        serial = Serializer(os.getenv("SECRET_KEY"))
        return serial.dumps({'user_id': self.id})

    @staticmethod
    def verify_user_token(token, expiress_sec=1800):
        serial = Serializer(os.getenv("SECRET_KEY"))
        try:
            user_id = serial.loads(token, max_age=expiress_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'status': 0,'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            print(data)
            active_user = User.query.filter_by(id=data['id']).first()
            if active_user.is_deleted == True :
                return jsonify({'status': 0,'message': 'Account with this email is deleted'})
                     
        except:
            return jsonify({'status': 0,'message': 'token is invalid'})

        return f(active_user, *args, **kwargs)

    return decorator

class Contact_us(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    message=db.Column('message', db.Text)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    read=db.Column('read', db.Boolean)
    created_at=db.Column(db.DateTime)
    updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow())

    def as_dict(self):
        user=User.query.filter_by(id=self.user_id).first()
        return{
            "id":self.id,
            "message":self.message,
            'fullname':user.fullname
        }

class Mind(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    sub_cat=db.Column(db.String(150),nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def as_dict(self):
        return{

            'id':self.id,
            'sub_cat':self.sub_cat
    }

class MindSubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=True)
    tags = db.Column(db.Text, nullable=True)
    reject_reason = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(150), nullable=True)
    likes = db.Column(db.Integer, default=0)
    reply = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    mind_id = db.Column(db.Integer, db.ForeignKey('mind.id', ondelete='CASCADE', onupdate='CASCADE'))
    admin_review_status = db.Column(db.String(150), nullable=True)
    report_count = db.Column(db.Integer, default=0)
    is_last_suggestion = db.Column(db.Boolean, default=0)  # Indicates if the post is inappropriate
    random_name = db.Column(db.String(150), nullable=True)
    random_image = db.Column(db.String(150), nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    type = db.Column(db.String(50), nullable=False)

    # question is for reflact type feild
    question = db.Column(db.Text, nullable=True)

    # question is for listen type feild
    transcript = db.Column(db.Text, nullable=True)
    trans_audio = db.Column(db.String(150), nullable=True)
    audio_file = db.Column(db.String(150), nullable=True)
    sub_category_like_data = db.relationship('MindSubCategorylikes', backref='sub_category_like_data')

    def as_dict(self,active_user):
        user = User.query.filter_by(id=self.user_id).first()

        if self.type == "Reflect":

            is_my_post = False
            if user.id == active_user.id:
                is_my_post = True

            # reply = Replies.query.filter_by(user_id=active_user.id,reflect_id=self.id).first()
            # if reply or self.user_id == active_user.id:
            #      replies = Replies.query.filter_by(reflect_id=self.id).all()

            replies = Replies.query.filter_by(reflect_id=self.id).count()

            return {
                'id': self.id,
                'question': self.question,
                'tags': self.tags,
                'username': user.username,
                "trans_audio": "",
                "created_at": self.created_at,
                "likes": self.likes if self.likes is not None else 0,
                "audio_file": "",
                "replies": replies,
                'profile_pic': COMMON_URL + "/static/profile_pic/" + user.image_name if user.image_name is not None else '',
                'report_count': self.report_count if self.report_count is not None else 0,
                'post_type': self.type.lower(),
                "transcript": "",
                'random_name': self.random_name,
                'random_image': COMMON_URL + self.random_image.replace('base', '') if self.random_image else "",
                'anonymous_status': self.is_anonymous,
                "admin_review_status": self.admin_review_status,
                'audio_duration': "",
                'is_my_post': is_my_post,
                'is_my_like': False
            }

        else:
            return {
                'id': self.id,
                'title': self.title,
                'tags': self.tags,
                'transcript': self.transcript,
                'username': user.username,
                "likes": self.likes if self.likes is not None else '0',
                'audio_file': COMMON_URL + "/static/audio/" + self.audio_file if self.audio_file else "",
                'profile_pic': COMMON_URL + "/static/profile_pic/" + user.image_name if user.image_name else "",
                'trans_audio': COMMON_URL + "/static/audio/" + self.trans_audio if self.trans_audio else "",
                'report_count': self.report_count,
                # 'is_last_suggestion':self.is_last_suggestion,
                'random_name': self.random_name if self.random_name is not None else '',
                'random_image': COMMON_URL + self.random_image.replace('base', '') if self.random_image else "",
                "admin_review_status": self.admin_review_status,
                'post_type': self.type.lower()
            }

class Reflect(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=True)
    tags=db.Column(db.Text,nullable=True)
    reject_reason=db.Column(db.Text,nullable=True)

    question=db.Column(db.Text,nullable=True)

    image_file=db.Column(db.String(150),nullable=True)
    likes=db.Column(db.Integer,nullable=True)
    reply=db.Column(db.Text,nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    mind_id = db.Column(db.Integer, db.ForeignKey('mind.id', ondelete='CASCADE', onupdate='CASCADE'))
    admin_review_status=db.Column(db.String(150),nullable=True)
    report_count = db.Column(db.Integer, default=0)
    is_last_suggestion = db.Column(db.Boolean, default=0)  # Indicates if the post is inappropriate
    random_name=db.Column(db.String(150),nullable=True)
    random_image=db.Column(db.String(150),nullable=True)
    is_anonymous=db.Column(db.Boolean,default=False)
    
    def as_dict(self,active_user):
        user=User.query.filter_by(id=self.user_id).first()

        is_my_post = False
        if user.id == active_user.id:
            is_my_post = True

        # reply = Replies.query.filter_by(user_id=active_user.id,reflect_id=self.id).first()
        # if reply or self.user_id == active_user.id:
        #      replies = Replies.query.filter_by(reflect_id=self.id).all()

        replies = Replies.query.filter_by(reflect_id=self.id).count()

        return{
            'id':self.id,
            'question':self.question,
            'tags':self.tags,
            'username':user.username,
            "trans_audio": "",
            "created_at": self.created_at,
            "likes":self.likes if self.likes is not None else 0,
            "audio_file": "",
            "replies": replies,
            'profile_pic': COMMON_URL+ "/static/profile_pic/" +user.image_name if user.image_name is not None else '',
            'report_count':self.report_count if self.report_count is not None else 0,
            'post_type': 'reflect',
            "transcript": "",
            'random_name':self.random_name,
            'random_image':COMMON_URL + self.random_image.replace('base/','') if self.random_image else "",
            'anonymous_status':self.is_anonymous,
            "admin_review_status":self.admin_review_status,
            'audio_duration': "",
            'is_my_post': is_my_post,
            'is_my_like': False
        }

class Listen(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=True)
    tags=db.Column(db.Text,nullable=True)
    reject_reason=db.Column(db.Text,nullable=True)

    transcript=db.Column(db.Text,nullable=True)
    trans_audio = db.Column(db.String(150),nullable=True)

    image_file=db.Column(db.String(150),nullable=True)

    audio_file=db.Column(db.String(150),nullable=True)

    likes=db.Column(db.Integer,nullable=True)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    mind_id = db.Column(db.Integer, db.ForeignKey('mind.id', ondelete='CASCADE', onupdate='CASCADE'))
    admin_review_status=db.Column(db.String(150),nullable=True)
    report_count = db.Column(db.Integer, default=0)
    is_last_suggestion = db.Column(db.Boolean, default=0)  #for reportpost   Indicates if the post is is_last_suggestion
    random_name=db.Column(db.String(150),nullable=True)
    random_image=db.Column(db.String(150),nullable=True)
    is_anonymous=db.Column(db.Boolean,default=False)

    def as_dict(self,active_user):
        user=User.query.filter_by(id=self.user_id).first()

        return{
                'id':self.id,
                'title':self.title,
                'tags':self.tags,
                'transcript':self.transcript,
                'username':user.username,
                "likes":self.likes if self.likes is not None else '0',
                'audio_file':self.audio_file,
                'profile_pic': COMMON_URL + "/static/profile_pic/"+user.image_name  if user.image_name else "",
                'trans_audio':COMMON_URL + "/static/audio/"+self.trans_audio  if self.trans_audio else "",
                'report_count':self.report_count,
                # 'is_last_suggestion':self.is_last_suggestion,
                'random_name':self.random_name if self.random_name is not None else '',
                'random_image':COMMON_URL + self.random_image.replace('base/','') if self.random_image else "",
                "admin_review_status":self.admin_review_status,
                'post_type' : 'listen'
            }

# class Reflect_likes(db.Model):
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
#
#     # reflect_id=db.Column(db.Integer,db.ForeignKey('reflect.id',ondelete='CASCADE',onupdate='CASCADE'))
#     reflect_id = db.Column(db.Integer, db.ForeignKey('mind_sub_category.id', ondelete='CASCADE', onupdate='CASCADE'))
#
#     created_at=db.Column(db.Date)
#     updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow())
#
#     def as_dict(self):
#         return{
#             "id":self.id,
#             "reflect_id":self.reflect_id,
#             "created_at":self.created_at.strftime("%b %d,%Y")
#         }

class MindSubCategorylikes(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))

    # reflect_id=db.Column(db.Integer,db.ForeignKey('reflect.id',ondelete='CASCADE',onupdate='CASCADE'))
    sub_cat_id = db.Column(db.Integer, db.ForeignKey('mind_sub_category.id', ondelete='CASCADE', onupdate='CASCADE'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete='CASCADE', onupdate='CASCADE'))

    created_at=db.Column(db.Date)
    updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow())

    def as_dict(self,active_user):

        if self.type == "body":
            return self.exercise_like_data.as_dict()
        else:
            return self.sub_category_like_data.as_dict(active_user)

        # return{
        #     "id":self.id,
        #     "reflect_id":self.reflect_id,
        #     "created_at":self.created_at.strftime("%b %d,%Y")
        # }

    def as_dict_reflect(self):
        return{
              "id":self.id,
              "reflect_id":self.sub_cat_id,
              "created_at":self.created_at.strftime("%b %d,%Y")
                    }

    def as_dict_listen(self):
        return{
            "id":self.id,
            "listen_id":self.sub_cat_id,
            "created_at":self.created_at.strftime("%b %d,%Y")
        }

# class Listen_likes(db.Model):
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
#
#     # listen_id=db.Column(db.Integer,db.ForeignKey('listen.id',ondelete='CASCADE',onupdate='CASCADE'))
#     listen_id = db.Column(db.Integer, db.ForeignKey('mind_sub_category.id', ondelete='CASCADE', onupdate='CASCADE'))
#
#     created_at=db.Column(db.Date)
#     updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow())
#
#     def as_dict(self):
#         return{
#             "id":self.id,
#             "listen_id":self.listen_id,
#             "created_at":self.created_at.strftime("%b %d,%Y")
#         }
          
def convert_tz():
    return datetime.now(tz=pytz.timezone('Asia/Kolkata'))

now = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
utcnow = datetime.now().astimezone().now()
print(utcnow)
    
class Session(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date)
    session_type=db.Column(db.String(150))
    time_start=db.Column(db.DateTime)
    time_end=db.Column(db.DateTime)
    total_time=db.Column(db.Integer)
    status=db.Column(db.String(50))
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))

    def as_dict(self):
        # print(self.time_end)
        print(utcnow)
        print(self.time_start)
        if self.time_start > utcnow:
            self.status = 'Upcoming'
            db.session.commit()
        elif self.time_start <= utcnow and self.time_end >= utcnow :    
            self.status = 'Active'
            db.session.commit()
        elif self.time_end < utcnow:
            self.status = 'Past'
            db.session.commit()

        user=User.query.filter_by(id=self.user_id).first()

        return{
            'id':self.id,
            'username':user.username,
            'date':self.date,
            'session_type':self.session_type,
            'time_start':self.time_start,
            'time_end':self.time_end,
            'total_time':self.total_time,
            'status':self.status,
            "created_at":self.created_at.strftime("%b %d,%Y")
        }

class Playlist(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    playlist_name=db.Column(db.String(150))
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))    
    exe_id=db.Column(db.Integer,db.ForeignKey('exercise.id',ondelete='CASCADE',onupdate='CASCADE'))

    def as_dict(self):
        exe=Exercise.query.filter_by(id=self.exe_id).first()
        return{
            'id':self.id,
            'playlist_name':self.playlist_name,
            'title':exe.title,
            'description':exe.description,
            'tags':exe.tags,
            'audio_file':exe.audio_file,
  }

class Report_post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    sub_cat_id = db.Column(db.Integer, db.ForeignKey('mind_sub_category.id', ondelete='CASCADE', onupdate='CASCADE'))
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def as_dict(self):
        user = User.query.filter_by(id=self.user_id).first()

        return {
            'id': self.id,
            'message': self.message,
            'user': user.username,
        }

class Replies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.Text,nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    # reflect_id = db.Column(db.Integer, db.ForeignKey('reflect.id', ondelete='CASCADE', onupdate='CASCADE'))

    reflect_id = db.Column(db.Integer, db.ForeignKey('mind_sub_category.id', ondelete='CASCADE', onupdate='CASCADE'))

    created_at = db.Column(db.DateTime)
    upfdated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def as_dict(self,active_user):
        # reflect = Reflect.query.filter_by(id=self.reflect_id).first()

        reflect = MindSubCategory.query.filter_by(id=self.reflect_id).first()

        user = User.query.filter_by(id=self.user_id).first()

        is_my_reply = False

        if active_user.id == self.user_id:
            is_my_reply = True

        return {
            'id': self.id,
            'reflect_id': reflect.id,
            'reply': self.reply,
            'user': user.username,
            'profile_pic': COMMON_URL+"/static/profile_pic/"+user.image_name if user.image_name else "",
            'create_time': self.created_at.strftime("%b %d,%Y"),
            'is_my_reply': is_my_reply
        }

class Feedback(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    message=db.Column('message', db.Text)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    read=db.Column('read', db.Boolean)
    date=db.Column(db.Date)
    time=db.Column(db.DateTime)
    created_at=db.Column(db.DateTime)
    updated_at=db.Column(db.DateTime,onupdate=datetime.utcnow())

    def as_dict(self):
        user=User.query.filter_by(id=self.user_id).first()
        return{
            "id":self.id,
            "message":self.message,
            'fullname':self.feed.fullname,
            'email':user.email,
            "read":self.read,
            "time":self.time.strftime("%b %d,%Y %H:%M:%S") if self.time else "",
            "created_at":self.created_at.strftime("%b %d,%Y") if self.created_at else ""
        }

class Notification(db.Model):
    id = db.Column('id', db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    title = db.Column(db.String(200))
    message = db.Column(db.String(500))
    page = db.Column(db.String(100))
    is_read = db.Column(db.Boolean(), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id', ondelete='CASCADE', onupdate='CASCADE'))
    sub_cat_id = db.Column(db.Integer, db.ForeignKey('mind_sub_category.id', ondelete='CASCADE', onupdate='CASCADE'))

    by_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
                      nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
                      nullable=False)

    def as_dict(self):
        user=User.query.filter_by(id=self.user_id).first()
        return{
            "id":self.id,
            "message":self.message,
            'profile_pic':COMMON_URL + "/static/profile_pic/"+user.image_name  if user.image_name else "",
            'title':self.title,
            "is_read":self.is_read,
            "created_at":self.created_at.strftime("%b %d,%Y") if self.created_at else ""
        }