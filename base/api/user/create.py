from flask import Blueprint, request, jsonify
from base.database.db import db
from base.api.user.models import MindSubCategorylikes,MindSubCategory,Contact_us, token_required, Reflect, Listen,Session, Playlist, Report_post, Replies, Feedback, User
from base.admin.models import Exercise
from datetime import datetime ,timedelta
from flask_login import login_required
import os
from werkzeug.security import secrets
from PIL import Image
import pyttsx3
from base.api.user.anonymous_names import random_name
import random
from sqlalchemy import or_

user_create = Blueprint('user_create', __name__)

ADMIN_PROFILE = 'base/static/admin_profile/'

AUDIO_FOLDER = "base/static/audio/"

AVTAR_IMAGE='base/static/avtar_pic/'

@user_create.route('/user/contact_us',methods=['POST'])
@token_required
def contact_us(active_user):

    data = request.get_json()
    message=data.get('message')

    if not message:
        return jsonify({'status': 0,'message': "Please provide your message"})

    message_report=Contact_us(message=message,created_at=datetime.today(),read=False, user_id=active_user.id)
    db.session.add(message_report)
    db.session.commit()

    return jsonify({'status':1,'message':'message Added Successfully.','data':message_report.as_dict()})

def save_audio(exercise_audio):

    random_hex=secrets.token_hex(8)
    _,f_ext = os.path.splitext(exercise_audio.filename)
    picture_fn=random_hex + f_ext
    audio_path = os.path.join(AUDIO_FOLDER, picture_fn)
    exercise_audio.save(audio_path)

    return picture_fn

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path = os.path.join(ADMIN_PROFILE,picture_fn)
    i=Image.open(form_picture)
    i = i.resize((500, 500))
    i.save(picture_path)

    return picture_fn

def random_image(directory):
    image_files = []
    for file in os.listdir(directory):
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            image_files.append(os.path.join(directory, file))

    if not image_files:
        print("No image files found in the directory.")
        return None

    random_file = random.choice(image_files)
    print(random_file)
    return random_file

@user_create.route("/user/mind/add_reflect_exercise", methods=['POST'])
@token_required
def add_reflect_exercise(active_user):
    anonymous = request.form.get('anonymous_status')
   
    directory = AVTAR_IMAGE

    mind_id = request.form.get('mind_id',2)
    question = request.form.get('question')
    likes = request.form.get('likes')
    tags = str(request.form.get('tags'))
    print(tags)
    tags = tags.split(',')
    tag_str = ""

    for tag in tags:
        tag_str += f"#{tag},"

    # exercise = Reflect(question=question,admin_review_status="under_review",tags=tag_str,likes=likes,created_at=datetime.utcnow(),user_id=active_user.id,mind_id=mind_id)

    exercise = MindSubCategory(type="Reflect",question=question,admin_review_status="under_review",tags=tag_str,likes=likes,created_at=datetime.utcnow(),user_id=active_user.id,mind_id=mind_id)

    db.session.add(exercise)
    db.session.commit()

    if anonymous == '1':
        exercise.is_anonymous=True
        randomname = random_name()
        randomimage = random_image(directory)

        exercise.random_name = randomname
        exercise.random_image = randomimage
        db.session.commit()

    return jsonify({'status': 1, 'message': 'Exercise added successfully.', 'data': exercise.as_dict(active_user)})

@user_create.route('/user/edit_reflect_category',methods=['POST'])
@token_required
def edit_reflect_category(active_user):

    directory = AVTAR_IMAGE

    relflcet_id = request.form.get('relflcet_id')
    if not relflcet_id:
        return jsonify({'status': 0,'message': 'Please select specific reflect data'})

    # sub_cat=Reflect.query.get(relflcet_id)

    sub_cat = MindSubCategory.query.get(relflcet_id)

    if sub_cat:
        sub_cat.question=request.form.get('question')
        sub_cat.admin_review_status = 'under_review'
        sub_cat.anonymous = request.form.get('anonymous_status')
        # sub_cat.reply=request.form.get('reply')
        tags = str(request.form.get('tags'))
        tags = tags.split(',')
        
        tag_str = ""
        for tag in tags:
            tag_str += f"#{tag},"
            sub_cat.tags = tag_str
            db.session.commit()

            if sub_cat.anonymous == '1': 
                sub_cat.is_anonymous=True
                randomname = random_name()
                randomimage = random_image(directory)

                sub_cat.random_name = randomname
                sub_cat.random_image = randomimage
                db.session.commit()

        return jsonify({'status':1,'message':'exercise added Successfully.','data':sub_cat.as_dict(active_user)})
    else :
        return jsonify({'status':0,'message':'there is no reflect post with specified id'})

@user_create.route('/user/reflect_likes',methods=["POST"])
@token_required
def likes(active_user):

    data = request.get_json()

    reflect_id = data.get('reflect_id')
    if not reflect_id:
        return jsonify({'status': 0,'message': 'Please select post first'})

    # post= Reflect.query.get(reflect_id)
    post = MindSubCategory.query.filter_by(id=reflect_id,type="Reflect").first()
    if not post:
        return jsonify({'status': 0,'message': 'Invalid post'})

    # like =Reflect_likes.query.filter_by(user_id=active_user.id, reflect_id=reflect_id).first()
    like = MindSubCategorylikes.query.filter_by(user_id=active_user.id, sub_cat_id=reflect_id,type='reflect').first()

    if like is None:
        if post.likes is not None:
            post.likes += 1
        else:
            post.likes = 1
        like = MindSubCategorylikes(type='reflect',user_id=active_user.id, sub_cat_id=reflect_id, created_at=datetime.utcnow())
        db.session.add(like)
        db.session.commit()

        return jsonify({'status': 1, 'message': 'Liked', 'data': like.as_dict_reflect(),'likes':post.likes})
            
    elif like is not None:
        if post.likes is not None:
            post.likes -= 1
        else:
            post.likes = 0
        db.session.delete(like)
        db.session.commit()
        return jsonify({'status': 0, 'message': 'Unliked', 'data': like.as_dict_reflect(),'likes':post.likes})

@user_create.route('/reflect/replies_list', methods=['GET', 'POST'])
@token_required
def reflect_replies_list(active_user):

    data = request.get_json()

    reflect_id = data.get('reflect_id')
    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    if not reflect_id:
        return jsonify({'status': 0,'message': 'Please select reflect first'})

    get_replies = Replies.query.filter_by(reflect_id=reflect_id).order_by(
        Replies.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    reply_list = [ i.as_dict(active_user) for i in get_replies.items ]

    pagination_info = {
            "current_page": get_replies.page,
            "has_next": get_replies.has_next,
            "has_prev": get_replies.has_prev,
            "total_pages": get_replies.pages,
            "total_items": get_replies.total
        }

    data = {
        'items': reply_list,
        'pagination': pagination_info
    }

    return jsonify({'status': 1,'message': "Success",'data': data})

@user_create.route('/user/reflect_reply', methods=['GET', 'POST'])
@token_required
def reflect_reply(active_user):

    data = request.get_json()
    reflect_id=data.get('reflect_id')
    reply = data.get('reply')

    # Check if the user has already replied within the last 12 hours
    last_reply = Replies.query.filter_by(reflect_id=reflect_id, user_id=active_user.id).order_by(Replies.created_at.desc()).first()

    if last_reply is not None and last_reply.created_at + timedelta(hours=12) > datetime.utcnow():
        return jsonify({'status': '0', 'message': 'You can only reply to this content once every 12 hours.'})

    new_reply = Replies(reply=reply, user_id=active_user.id, reflect_id=reflect_id,created_at=datetime.utcnow())
    db.session.add(new_reply)
    db.session.commit()

    all_replies = Replies.query.filter_by(reflect_id=reflect_id).all()

    return jsonify({'status': 1, 'message': 'Reply added successfully.', 'all_replies': [r.reply for r in all_replies]})

def convert_text_to_audio(transcript):
    random_hex = secrets.token_hex(16)
    filename = random_hex + '.mp3'
    file_path = os.path.join(AUDIO_FOLDER, random_hex + '.mp3')
    # Convert text to speech with a female voice
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Fiona')
    engine.save_to_file(transcript, file_path)
    engine.runAndWait()
    return filename

@user_create.route("/user/mind/add_listen_exercise",methods=['POST'])
@token_required
def add_listen_exercise(active_user):

    anonymous = request.form.get('anonymous_status')
   
    directory = AVTAR_IMAGE

    mind_id=request.form.get('mind_id',1)
    print(active_user)
    title = request.form.get('title')
    tags =(request.form.getlist('tags'))
    transcript=request.form.get('transcript')
    trans_audio = convert_text_to_audio(transcript)
    likes=request.form.get('likes')
    audio_file = request.files.get('audio_file')

    audio = None
    if audio_file:
        audio=save_audio(audio_file)
        print(audio)
    # exercise=Listen(title=title,transcript=transcript,trans_audio=trans_audio,admin_review_status="under_review",tags=tags,likes=likes, created_at=datetime.utcnow(),user_id=active_user.id, mind_id=mind_id,audio_file=audio)

    exercise=MindSubCategory(type="Listen",title=title,transcript=transcript,trans_audio=trans_audio,admin_review_status="under_review",tags=tags,likes=likes, created_at=datetime.utcnow(),user_id=active_user.id, mind_id=mind_id,audio_file=audio)

    db.session.add(exercise)
    db.session.commit()

    if anonymous == '1':
        exercise.is_anonymous=True
        randomname = random_name()
        randomimage = random_image(directory)

        exercise.random_name = randomname
        exercise.random_image = randomimage
        db.session.commit()

    return jsonify({'status':1,'message':'exercise added Successfully.','data':exercise.as_dict(active_user)})

@user_create.route('/user/edit_listen_category',methods=['GET','POST'])
@token_required
def edit_listen_category(active_user):

    directory = AVTAR_IMAGE

    listen_id=request.form.get('listen_id')
    if not listen_id:
        return jsonify({'status': 0,'message': 'Please select content first'})

    # sub_cat = Listen.query.get(listen_id)

    sub_cat = MindSubCategory.query.get(listen_id)

    if not sub_cat:
        return jsonify({'status': 0,'message': 'Invalid data'})

    sub_cat.anonymous = request.form.get('anonymous_status')
    sub_cat.title=request.form.get('title')
    transcript=request.form.get('transcript')
    sub_cat.trans_audio = convert_text_to_audio(transcript)
    sub_cat.transcript = transcript
    sub_cat.audio_file = None
    audio_file = request.files.get('audio')
    tags = str(request.form.get('tags'))
    tags = tags.split(',')
    sub_cat.admin_review_status = 'under_review'
        
    tag_str = ""
    for tag in tags:
        tag_str += f"#{tag},"
    sub_cat.tags = tag_str

    if audio_file:
        audio = save_audio(audio_file)
        sub_cat.audio_file = audio
    db.session.commit()

    if sub_cat.anonymous == '1':
        sub_cat.is_anonymous=True
        randomname = random_name()
        randomimage = random_image(directory)

        sub_cat.random_name = randomname
        sub_cat.random_image = randomimage
        db.session.commit()
            
    return jsonify({'status':1,'message':'Exercise updated successfully.','data':sub_cat.as_dict(active_user)})

@user_create.route('/user/listen_likes',methods=["POST"])
@token_required
def listen_likes(active_user):

    data = request.get_json()

    listen_id = data.get('listen_id')

    if not listen_id:
        return jsonify({'status': 0,'message': 'Please select post first'})

    # post= Listen.query.get(listen_id)
    post = MindSubCategory.query.filter_by(id=listen_id,type="Listen").first()
    if not post:
        return jsonify({'status': 0,'message': 'Invalid post'})

    like = MindSubCategorylikes.query.filter_by(user_id=active_user.id, sub_cat_id=listen_id,type='listen').first()

    if like is None:
        if post.likes is not None:
            post.likes += 1
        else:
            post.likes = 1
        like = MindSubCategorylikes(type='listen',user_id=active_user.id, sub_cat_id=listen_id,created_at=datetime.utcnow())
        db.session.add(like)
        db.session.commit()

        return jsonify({'status': 1, 'message': 'Liked', 'data': like.as_dict_listen(),'likes':post.likes})
            
    elif like is not None:
        if post.likes is not None:
            post.likes -= 1
        else:
            post.likes = 0
        db.session.delete(like)
        db.session.commit()

        return jsonify({'status': 0, 'message': 'Unliked', 'data': like.as_dict_listen(),'likes':post.likes})

@user_create.route('/user/add_status_category',methods=['POST'])
@login_required
def add_status_category():
    status=request.form.get('status')
    type=Session(status=status)
    db.session.add(type)
    db.session.commit()

    return jsonify({'status':1,'message':'status added Successfully.'})

@user_create.route("/user/add_session",methods=['GET','POST'])
@token_required
def add_session(active_user):
    if request.method =="POST":
        date=request.form.get('date')
        session_type = request.form.get('session_type')
        time_start =datetime.strptime(request.form.get('time_start'), '%Y-%m-%d %H:%M:%S')
        time_end=datetime.strptime(request.form.get('time_end'), '%Y-%m-%d %H:%M:%S')
        status=request.form.get('status')
        total_time=(time_end - time_start)
        total_time = total_time.seconds
        print(total_time)

        my_session=Session(date=date,session_type=session_type,time_start=time_start,time_end=time_end,status=status,total_time=total_time,created_at=datetime.utcnow(),user_id=active_user.id)
        db.session.add(my_session)
        db.session.commit()
        print(datetime.utcnow())

        return jsonify({'status':1,'message':'sesson added Successfully.','data':my_session.as_dict()})

@user_create.route('/user/playlists', methods=['POST'])
@token_required
def create_playlist(active_user):
    data = request.get_json()
    exercise_ids = data.get('exercise_ids')
    playlist_name = data.get('playlist_name')

    if not playlist_name:
        return jsonify({'message': 'Playlist name is required'})

    playlist_list = []

    for exercise_id in exercise_ids:

        exercise = Exercise.query.filter_by(id=exercise_id).first()
        if not exercise:
            return jsonify({'message': f'Exercise with ID {exercise_id} does not exist'})

        playlist = Playlist(playlist_name=playlist_name, exe_id=int(exercise_id), user_id=active_user.id, created_at=datetime.now())
        db.session.add(playlist)
        db.session.commit()
        playlist_list.append(playlist.as_dict())

    return jsonify({'message': 'Playlist created successfully', 'playlist': playlist_list})

@user_create.route('/user/report_post', methods=['POST'])
@token_required
def report_post(active_user):
    data = request.get_json()

    # Extract the necessary information from the request
    post_type = data.get('post_type')  # 'reflect' or 'listen'
    post_id = data.get('post_id')
    message = data.get('message')

    post = Report_post.query.filter_by(user_id=active_user.id, sub_cat_id=post_id,type = post_type).first()

    # if post_type == 'reflect':
    #     post = Report_post.query.filter_by(user_id=active_user.id,reflect_id=post_id).first()
    # elif post_type == 'listen':
    #     post = Report_post.query.filter_by(user_id=active_user.id,listen_id=post_id).first()
    # else:
    #     post = None
        
    if post :
        return jsonify({'status': 0, 'message': 'You have already reported this post'})
    else :
        report = Report_post(message=message, user_id=active_user.id, created_at=datetime.now(),type=post_type,sub_cat_id=post_id)

        # if post_type == 'reflect':
        #     report.reflect_id = post_id
        #     post = MindSubCategory.query.filter_by(id=post_id,type="Reflect").first()
        # elif post_type == 'listen':
        #     report.listen_id = post_id
        #     post = MindSubCategory.query.filter_by(id=post_id,type="Listen").first()

        db.session.add(report)
        db.session.commit()

        post = MindSubCategory.query.filter_by(id=post_id, type="Reflect").first()

        # Check the report count for the post
        report_count = Report_post.query.filter_by(
            sub_cat_id=post.id,type=post
        ).count()

        # Specify the report threshold

        # report_threshold = 5

        # if report_count >= report_threshold:
        #     # Take action to mark the post as last suggestion or remove it
        #     post.is_last_suggestion = True  # Add an 'is_last_suggestion' field to your post model
        #     db.session.commit()

        #     # Additional action, e.g., removing the post
        #     # db.session.delete(post)
        #     # db.session.commit()

        #     return jsonify({'status': 0, 'message': 'This post has'})

        # Save the updated report count to the post
        post.report_count = report_count
        db.session.commit()

        return jsonify({'status': 1, 'message': 'Post reported successfully', 'data': report.as_dict(), 'total_reports': report_count})

@user_create.route('/user/feedback',methods=['POST'])
@token_required
def feedback(active_user):

    if request.method=='POST':
        data = request.get_json()
        message=data.get('feedback_message')
        message_report=Feedback(message=message,created_at=datetime.utcnow(),read=False, user_id=active_user.id,time = datetime.utcnow())
        db.session.add(message_report)
        db.session.commit()
        return jsonify({'status':'1','message':'message Added Successfully.','data':message_report.as_dict()})

@user_create.route("/user/delete_account", methods=['POST'])
@token_required
def delete_account(active_user):
    if request.method=='POST':
        user=User.query.filter_by(id=active_user.id).first()
    # Soft delete the user account
        if user:
            if user.is_deleted==False:
        
               user.is_deleted=True 
               db.session.commit()
               return jsonify({'status': 1, 'message': 'Account deleted successfully.'})
            else:
                return jsonify({'status': 1, 'message': 'Account already deleted.'})   
    else:

        return jsonify({'status': 1, 'message': 'no user found'})

@user_create.route('/user/body_likes',methods=["POST"])
@token_required
def body_likes(active_user):
    if request.method=='POST':
        data = request.get_json()  

        exercise_id = data.get('exercise_id')
        if not exercise_id:
            return jsonify({'status':0,'message': 'Please select post first'})

        post= Exercise.query.get(exercise_id)
        if not post:
            return jsonify({'status':0,'message': 'Invalid post'})

        # like = Body_likes.query.filter_by(user_id=active_user.id, exercise_id=exercise_id).first()

        like = MindSubCategorylikes.query.filter_by(user_id=active_user.id, exercise_id=exercise_id,type="body").first()

        if like is None:
            if post.likes is not None:
                post.likes += 1
            else:
                post.likes = 1

            # add_like = Body_likes(user_id=active_user.id, exercise_id=exercise_id,created_at=datetime.utcnow())

            add_like = MindSubCategorylikes(type='body',user_id=active_user.id, exercise_id=exercise_id, created_at=datetime.utcnow())

            db.session.add(add_like)
            db.session.commit()
            return jsonify({'status': 1, 'message': 'Liked', 'data': like.as_dict(),'likes':post.likes})
            
        elif like is not None:
            if post.likes is not None:
                post.likes -= 1
            else:
                post.likes = 0
            db.session.delete(like)
            db.session.commit()
            return jsonify({'status': 0, 'message': 'Unliked', 'data': like.as_dict(),'likes':post.likes})

@user_create.route("/user/mind/search_exercises", methods=['POST'])
@token_required
def search_exercises(active_user):
    if request.method == "POST":
        search_keyword = request.get_json().get('keyword')
        
        reflect_exercises = Reflect.query.join(User).filter(or_(User.username.ilike(f'%{search_keyword}%'),Reflect.question.ilike(f'%{search_keyword}%'),Reflect.tags.ilike(f'%{search_keyword}%'),)).all()

        listen_exercises = Listen.query.join(User).filter(or_(User.username.ilike(f'%{search_keyword}%'),Listen.title.ilike(f'%{search_keyword}%'),Listen.tags.ilike(f'%{search_keyword}%'),Listen.transcript.ilike(f'%{search_keyword}%'))).all()

        exercises = reflect_exercises + listen_exercises

    
        exercise_data = [exercise.as_dict(active_user) for exercise in exercises]
        if exercise_data:

            return jsonify({'status': 1, 'message': 'Exercise found successfully.', 'data': exercise_data})
        else:
            return jsonify({'status': 1, 'message': 'No result Found'})

@user_create.route('/user/search_body_exericse', methods=['GET'])
@token_required
def search_event(active_user):
    data = request.get_json() 
    search_keyword=data['keyword']
    query = Exercise.query.filter(or_(Exercise.title.ilike(f"%{search_keyword}%"), Exercise.tags.ilike(f"%{search_keyword}%"),Exercise.description.ilike(f"%{search_keyword}%")))
    searched = query.all()
    if searched:
        return jsonify({'status': 1, 'message': 'your searched  is ', 'data': [i.as_dict(active_user) for i in searched]}) 
    else:
        return jsonify({'status': 0, 'message': 'no result found'})