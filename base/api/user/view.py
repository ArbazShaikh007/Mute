from flask import Blueprint,jsonify,request
from base.api.user.models import Notification,MindSubCategorylikes,MindSubCategory,Mind, Reflect, Listen, Session, User, token_required, Feedback
from base.admin.models import Exercise, Category
from base.database.db import db
from datetime import datetime
from random import random
from sqlalchemy import func, or_
# from base.

user_view = Blueprint('user_view', __name__)

@user_view.route("/get_notification_count", methods=['GET'])
@token_required
def get_notification_count(active_user):

    notification_count = Notification.query.filter_by(is_read=False,to_id = active_user.id).count()

    return jsonify({"status": 1, "message": "Success",'notification_count': notification_count})

@user_view.route("/my_notification_list", methods=['POST'])
@token_required
def my_notification_list(active_user):
    data = request.get_json()

    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    get_all_notification = Notification.query.filter_by(is_read=False,to_id = active_user.id).all()
    if len(get_all_notification)>0:
        for i in get_all_notification:
            i.is_read = True
        db.session.commit()

    get_notifications = Notification.query.filter_by(to_id = active_user.id).order_by(Notification.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    notification_list = [ i.as_dict() for i in get_notifications.items ]

    return {
        "status": 1,
        "message": "Success",
        "data": {
            "current_page": get_notifications.page,
            "has_next": get_notifications.has_next,
            "has_prev": get_notifications.has_prev,
            "total_pages": get_notifications.pages,
            "List": notification_list
        }
    }

@user_view.route("/user/body_exercise_page", methods=['POST'])
@token_required
def body_exercise_page(active_user):

    data = request.get_json()
    print('data',data)

    if not data:
        return jsonify({'status':0,'message': 'Json is empty'})

    search = data.get('search')

    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    if search:
        query = Exercise.query.filter(or_(
            Exercise.title.ilike(f"%{search}%"),
            func.replace(Exercise.tags, '#', '').ilike(f"%{search}%")
        )).order_by(Exercise.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    else:
        query = Exercise.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    exercise_data = [i.as_dict() for i in query.items]

    return {
        "status": 1,
        "message": "Success",
        "data": {
            "current_page": query.page,
            "has_next": query.has_next,
            "has_prev": query.has_prev,
            "total_pages": query.pages,
            "items": exercise_data
        }
    }

@user_view.route("/user/breathe_exercise_page", methods=['POST'])
@token_required
def breathe_exercise_page(active_user):

    data = request.get_json()

    print('data',data)

    search = data.get('search')
    cat_id = data.get('cat_id',1)

    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    if search:
        query = Exercise.query.filter(Exercise.cat_id==cat_id,or_(
            Exercise.title.ilike(f"%{search}%"),
            func.replace(Exercise.tags, '#', '').ilike(f"%{search}%")
        )).order_by(Exercise.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    else:
        query = Exercise.query.filter(Exercise.cat_id==cat_id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    brethe_data = [i.as_dict() for i in query.items]

    return {
        "status": 1,
        "message": "Success",
        "data": {
            "current_page": query.page,
            "has_next": query.has_next,
            "has_prev": query.has_prev,
            "total_pages": query.pages,
            "items": brethe_data
        }
    }

@user_view.route("/user/move_exercise_page", methods=['GET','POST'])
@token_required
def move_exercise_page(active_user):
    data = request.get_json()

    print('data', data)

    cat_id = data.get('cat_id',4)

    search = data.get('search')

    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    if search:
        query = Exercise.query.filter(Exercise.cat_id == cat_id, or_(
            Exercise.title.ilike(f"%{search}%"),
            func.replace(Exercise.tags, '#', '').ilike(f"%{search}%")
        )).order_by(Exercise.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    else:
        query = Exercise.query.filter(Exercise.cat_id == cat_id).order_by(Exercise.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    move_data = [i.as_dict() for i in query.items]

    return {
        "status": 1,
        "message": "Success",
        "data": {
            "current_page": query.page,
            "has_next": query.has_next,
            "has_prev": query.has_prev,
            "total_pages": query.pages,
            "items": move_data
        }
    }

@user_view.route("/user/mind_category_page", methods=['GET','POST'])
@token_required
def mind_category_page(active_user):

    data = request.get_json()
    print('data',data)

    search = data.get('search')

    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    # minds = Mind.query.all()

    if search:
        query = MindSubCategory.query.join(User, User.id == MindSubCategory.user_id).filter \
            (User.is_deleted != True,
             MindSubCategory.is_last_suggestion == False,
             or_(
                 MindSubCategory.title.ilike(
                     f"%{search}%"),
                 func.replace(
                     MindSubCategory.tags, '#', '').ilike(f"%{search}%"))).order_by(
            MindSubCategory.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    else:
        query = MindSubCategory.query.join(User, User.id == MindSubCategory.user_id).filter(User.is_deleted != True,
                                                                                            MindSubCategory.is_last_suggestion == False).order_by(
            MindSubCategory.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    mind_data = [i.as_dict(active_user) for i in query.items]

    return {
        "status": 1,
        "message": "Success",
        "data": {
            "current_page": query.page,
            "has_next": query.has_next,
            "has_prev": query.has_prev,
            "total_pages": query.pages,
            "items": mind_data
        }
    }

    # return jsonify({'status':1,'message':' Mind catagory List.','data':[i.as_dict() for i in minds]})

@user_view.route("/user/mind_reflect_page", methods=['POST'])
@token_required
def mind_reflect_page(active_user):
    data = request.get_json()
    print('data',data)

    mind_id = data.get('mind_id', 2)

    search = data.get('search')

    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    # reflect_exercises = Reflect.query.join(User,User.id==Reflect.user_id).filter(User.is_deleted != True ).filter_by(mind_id=2,is_last_suggestion=False).all()

    if search:
        query = MindSubCategory.query.join(User, User.id == MindSubCategory.user_id).filter \
            (User.is_deleted != True,
             MindSubCategory.type == "Reflect",
             MindSubCategory.mind_id == mind_id,
             MindSubCategory.is_last_suggestion == False,
             or_(
                 MindSubCategory.title.ilike(
                     f"%{search}%"),
                 func.replace(
                     MindSubCategory.tags, '#', '').ilike(f"%{search}%"))).order_by(
            MindSubCategory.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    else:
        query = MindSubCategory.query.join(User, User.id == MindSubCategory.user_id).filter(User.is_deleted != True,
                                                                                            MindSubCategory.type == "Reflect",
                                                                                            MindSubCategory.mind_id == mind_id,
                                                                                            MindSubCategory.is_last_suggestion == False).order_by(
            MindSubCategory.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    reflect_data = [i.as_dict(active_user) for i in query.items]

    return {
        "status": 1,
        "message": "Success",
        "data": {
            "current_page": query.page,
            "has_next": query.has_next,
            "has_prev": query.has_prev,
            "total_pages": query.pages,
            "items": reflect_data
        }
    }

    # return jsonify({'status':1,'message':'reflect displayed Successfully.','data':[i.as_dict(active_user) for i in reflect_exercises]})

@user_view.route("/user/mind_listen_page", methods=['GET','POST'])
@token_required
def mind_listen_page(active_user):
    try:
        data = request.get_json()
        print('data',data)
        mind_id = data.get('mind_id', 1)

        search = data.get('search')

        page = int(data.get('page', 1))
        per_page = int(data.get('per_page', 10))

        # listen_exercises = Listen.query.join(User,User.id==Listen.user_id).filter(User.is_deleted != True ,Listen.mind_id==1,Listen.is_last_suggestion==False).all()

        if search:
            query = MindSubCategory.query.join(User, User.id == MindSubCategory.user_id).filter\
                (User.is_deleted != True,
                    MindSubCategory.type == "Listen",
                    MindSubCategory.mind_id == mind_id,
                    MindSubCategory.is_last_suggestion == False,
                    or_(
                         MindSubCategory.title.ilike(
                         f"%{search}%"),
                         func.replace(
                                      MindSubCategory.tags,'#', '').ilike(f"%{search}%"))).order_by(
                MindSubCategory.id.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

        else:
            query = MindSubCategory.query.join(User,User.id==MindSubCategory.user_id).filter(User.is_deleted != True,MindSubCategory.type=="Listen" ,MindSubCategory.mind_id==mind_id,MindSubCategory.is_last_suggestion==False).order_by(MindSubCategory.id.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

        mind_listen_data = [i.as_dict(active_user) for i in query.items]

        return {
            "status": 1,
            "message": "Success",
            "data": {
                "current_page": query.page,
                "has_next": query.has_next,
                "has_prev": query.has_prev,
                "total_pages": query.pages,
                "items": mind_listen_data
            }
        }

        # return jsonify({'status':1,'message':'Success.','data':[i.as_dict(active_user) for i in query.items]})
    except Exception as e:
        print('errorrrrrrrrrrrrrrrrr:', str(e))
        return {'status': 0, 'message': 'Something went wrong'}, 500

@user_view.route("/user/session_page", methods=['GET','POST'])
def session_page(active_user):
    data = request.get_json()  
    session_id = data["session_id"]
    session = Session.query.filter_by(id=session_id).all()

    return jsonify({'status':1,'message':'Session added Successfully.','data':[i.as_dict() for i in session]})

# @user_view.route("/user/status_category_page", methods=['GET','POST'])
# def status_category_page():
#     minds=Mind.query.all()
#     return jsonify({'status':'1','message':'message deleted Successfully.','data':minds.as_dict()})

@user_view.route("/user/feedback_page", methods=['GET','POST'])
@token_required
def feedback_page(active_user):
    feedbacks=Feedback.query.filter_by(user_id=active_user.id).order_by(Feedback.id.desc()).all()
    return jsonify({'status':1,'message':'feedback list get  Successfully.','data': [i.as_dict() for i in feedbacks]})

@user_view.route("/user/default_playlist", methods=['GET','POST'])
@token_required
def default_playlist(active_user):
    default_list=Exercise.query.order_by(Exercise.id.desc()).limit(15)
    return jsonify({'status':1,'message':'Default Playlist','data': [i.as_dict() for i in default_list]})

@user_view.route('/user/reflect_history', methods=['POST'])
@token_required
def reflect_history(active_user):
    data = request.get_json()
    print('data',data)

    status_param = data.get("status")

    # page = int(data.get('page', 1))
    # per_page = int(data.get('per_page', 10))

    # posts = Reflect.query.filter_by(user_id=active_user.id,admin_review_status=status_param).all()

    # posts = MindSubCategory.query.filter_by(type="Reflect",user_id=active_user.id, admin_review_status=status_param).order_by(MindSubCategory.id.desc()).paginate(
    #             page=page,
    #             per_page=per_page,
    #             error_out=False
    #         )

    posts = MindSubCategory.query.filter_by(type="Reflect", user_id=active_user.id,
                                            admin_review_status=status_param).order_by(
        MindSubCategory.id.desc()).all()

    # data = [post.as_dict(active_user) for post in posts.items]

    data = [post.as_dict(active_user) for post in posts]

    # return {
    #     "status": 1,
    #     "message": "Success",
    #     "data": {
    #         "current_page": posts.page,
    #         "has_next": posts.has_next,
    #         "has_prev": posts.has_prev,
    #         "total_pages": posts.pages,
    #         "items": data
    #     }
    # }

    return jsonify({'status': 1, 'message': 'Success', 'data': data})

@user_view.route('/user/listen_history', methods=['POST'])
@token_required
def listen_history(active_user):
    data = request.get_json()

    status_param = data.get("status")

    # page = int(data.get('page', 1))
    # per_page = int(data.get('per_page', 10))

    # posts = Listen.query.filter_by(user_id=active_user.id,admin_review_status=status_param).all()



    # posts = MindSubCategory.query.filter_by(type="Listen",user_id=active_user.id, admin_review_status=status_param).order_by(MindSubCategory.id.desc()).paginate(
    #             page=page,
    #             per_page=per_page,
    #             error_out=False
    #         )

    posts = MindSubCategory.query.filter_by(type="Listen", user_id=active_user.id,
                                            admin_review_status=status_param).order_by(
        MindSubCategory.id.desc()).all()

    # data = [post.as_dict(active_user) for post in posts.items]

    # return {
    #     "status": 1,
    #     "message": "Success",
    #     "data": {
    #         "current_page": posts.page,
    #         "has_next": posts.has_next,
    #         "has_prev": posts.has_prev,
    #         "total_pages": posts.pages,
    #         "items": data
    #     }
    # }

    data = [post.as_dict(active_user) for post in posts]

    return jsonify({'status': 1, 'message': 'Success', 'data': data})

@user_view.route('/user/user_history', methods=['POST'])
@token_required
def user_history(active_user):
    data = request.get_json()

    status_param = data.get("status")

    # page = int(data.get('page', 1))
    # per_page = int(data.get('per_page', 10))

    # posts = MindSubCategory.query.filter_by(user_id=active_user.id, admin_review_status=status_param).order_by(MindSubCategory.id.desc()).paginate(
    #             page=page,
    #             per_page=per_page,
    #             error_out=False
    #         )

    posts = MindSubCategory.query.filter_by(user_id=active_user.id,
                                            admin_review_status=status_param).order_by(
        MindSubCategory.id.desc()).all()

    # data = [post.as_dict(active_user) for post in posts.items]

    # return {
    #     "status": 1,
    #     "message": "Success",
    #     "data": {
    #         "current_page": posts.page,
    #         "has_next": posts.has_next,
    #         "has_prev": posts.has_prev,
    #         "total_pages": posts.pages,
    #         "items": data
    #     }
    # }

    data = [post.as_dict(active_user) for post in posts]

    return jsonify({'status': 1, 'message': 'Success', 'data': data})

# @user_view.route("/user/user_liked_post", methods=['GET'])
# @token_required
# def user_liked_post(active_user):
#     listen_like_posts = Listen_likes.query.filter_by(user_id=active_user.id).order_by(Listen_likes.id.desc()).all()
#     reflect_like_posts = Reflect_likes.query.filter_by(user_id=active_user.id).order_by(Reflect_likes.id.desc()).all()
#     body_like_posts = Body_likes.query.filter_by(user_id=active_user.id).order_by(Body_likes.id.desc()).all()
#
#     data = []
#     if listen_like_posts:
#         data.extend(listen_like_posts)
#     if reflect_like_posts:
#         data.extend(reflect_like_posts)
#     if body_like_posts:
#         data.extend(body_like_posts)
#
#     liked_posts = [post.as_dict() for post in data]
#
#     return jsonify({'status': 1, 'message': 'Your liked posts list.', 'data': liked_posts})

@user_view.route("/user/Display_likes_list", methods=['POST'])
@token_required
def user_liked_post(active_user):
    data = request.get_json()

    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    liked_posts = MindSubCategorylikes.query.filter_by(user_id=active_user.id).order_by(MindSubCategorylikes.id.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

    # listen_like_posts = Listen_likes.query.filter_by(user_id=active_user.id).order_by(Listen_likes.id.desc()).all()
    # reflect_like_posts = Reflect_likes.query.filter_by(user_id=active_user.id).order_by(Reflect_likes.id.desc()).all()
    # body_like_posts = Body_likes.query.filter_by(user_id=active_user.id).order_by(Body_likes.id.desc()).all()
    #
    # data = []
    # if listen_like_posts:
    #     data.extend(listen_like_posts)
    # if reflect_like_posts:
    #     data.extend(reflect_like_posts)
    # if body_like_posts:
    #     data.extend(body_like_posts)

    liked_posts_list = [ post.as_dict(active_user) for post in liked_posts.items ]

    return {
        "status": 1,
        "message": "Success",
        "data": {
            "current_page": liked_posts.page,
            "has_next": liked_posts.has_next,
            "has_prev": liked_posts.has_prev,
            "total_pages": liked_posts.pages,
            "items": liked_posts_list
        }
    }

    # return jsonify({'status': 1, 'message': 'Your liked posts list.', 'data': liked_posts})