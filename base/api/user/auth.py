import jwt,os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, redirect, flash, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from base.database.db import db
from base.api.user.models import User
from datetime import datetime, timedelta
from base.api.user.models import token_required
from base.api.user.utils import send_reset_email
from werkzeug.utils import secure_filename
import secrets
import random
from base.common.utils import common_path
load_dotenv('/home/ArbazShaikh007/mysite/mute/base/.env')
UPLOAD_FOLDER="base/static/profile_pic/"
load_dotenv()

user_auth = Blueprint('user_auth',__name__)

@user_auth.route('/registration', methods=['POST'])
def registration():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        birthday = data.get('birthday')
        password = data.get('password')
        email = data.get('email')
        device_id = data.get('device_id')
        device_type = data.get('device_type')
        image_name = 'default.png'

        # Check if required fields are empty
        if not all([username, birthday, password, email,device_id,device_type]):
            return jsonify({'status': 0, 'message': 'All fields are required'})

        # Check if username is unique
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({'status': 0, 'message': 'Username is already taken'})

        # Check if the email is already taken
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({'status': 0, 'message': 'Email is already taken'})

        # Calculate age from birthday
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        
        # Create a new user
        hash_password = generate_password_hash(password)
        user_data = User(username=username, birthdate=birthday, email=email, device_id=device_id, device_type=device_type, password=hash_password, image_name=image_name, created_at=datetime.utcnow())
        db.session.add(user_data)
        db.session.commit()

        # verification_code = str(random.randint(1000, 9999))
        # welcome_mail(user_data,verification_code)

        token = jwt.encode(
            {'id': user_data.id, 'exp': datetime.utcnow() + timedelta(days=365)},os.getenv('SECRET_KEY')
        )

        return jsonify({'status': 1, 'message': 'Register successfully', 'data': user_data.as_dict(token)})

@user_auth.route('/user_login', methods=['POST'])
def user_login():
    if request.method=='POST':
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        device_id=data.get('device_id')
        device_type=data.get('device_type')

        if not email or not password:
            return {'status': 0, 'message': 'Email and password is required'}
            
        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_deleted == True:
                return jsonify({'status': 0, 'message': 'This account is deleted'})

        if not user:
            return {'status': 0, 'message': 'User doesn\'t exist !'}

        if user and check_password_hash(user.password,password) :

            user.device_id = device_id if  device_id != None or device_id != '' else user.device_id
            user.device_type = device_type if  device_type != None or device_type != '' else user.device_type

            db.session.commit()

            token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(days=365)}, os.getenv('SECRET_KEY'))

            return jsonify(
                {'status': 1, 'message': 'Login successfully', 'data': user.login_res(token)})

        elif user and user.is_block==True:

            return jsonify(
                {'status': 0, 'message': 'User is blocked'})
        else:
            return jsonify({'status': 0, 'message': 'Wrong password'})

@user_auth.route('/social_register', methods=['POST'])
def social_register():
    if request.method == 'POST':
        #stripe.api_key = 'sk_test_51MoURYABa0Gyguy70gzvVREJciYkqoeX18Gml2Wq8ySdo3VpdcDctQ3gIG3wDfqk1VLVD94KlPhq04unvPIeaIvd00DBVpNfrw'
        data=request.get_json()
        social_id = data.get('social_id')
        social_type = data.get('social_type')
        device_id = data.get('device_id')
        device_type = data.get('device_type')
        email = data.get('email')
        # birthday = data['birthday']
        username = data.get('username')
        image_name = 'default.jpg'

        
        user = User.query.filter_by(social_id=social_id).first()
        if user:
            if user.is_deleted == True:
                return jsonify({'status': 0, 'message': 'This account is deleted'})
        if user:
            token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(days = 365)}, os.getenv('SECRET_KEY'))
            return jsonify(
                {'status': 1, 'message': 'login successfully', 'data': user.login_res(token) })

        user_data = User(social_id=social_id,email= email,username=username,image_name = image_name,social_type=social_type,device_id=device_id,device_type=device_type,created_at=datetime.utcnow())

        db.session.add(user_data)
        db.session.commit()
        #social_welcome_mail(user_data)
        token = jwt.encode({'id': user_data.id, 'exp': datetime.utcnow() + timedelta(days = 365)}, os.getenv('SECRET_KEY'))

        return jsonify({'status': 1, 'message':'Register Successful','data': user_data.as_dict(token),'token':token })

@user_auth.route('/getuser', methods=['GET'])
@token_required
def getuser(active_user):
    token = request.headers.get('Authorization')
    return jsonify({'status': 1, 'message': 'success', 'data': active_user.user_data(token)})

@user_auth.route('/change_password', methods=['POST'])
@token_required
def change_password(active_user):
    data=request.get_json()
    old_pwd = data.get('oldPassword')
    new_pwd = data.get('newPassword')

    if not([old_pwd, new_pwd]):
        return jsonify({"status":0,'message':"missing data"})

    elif active_user and active_user.check_password(old_pwd):

        if new_pwd == old_pwd :
            return jsonify({'status': 0, 'message': 'New password must be different from previous password !'})

        else:
            hash_password = generate_password_hash(new_pwd)
            active_user.password = hash_password
            db.session.commit()

            return jsonify({'status': 1, 'message': 'Password changed successfully !'})
    else:
        return jsonify({'status': 0, 'message': 'Old password is wrong !'})

@user_auth.route('/user/reset_request', methods=['GET', 'POST'])
def user_reset_request():  
    if request.method == 'POST':
        data=request.get_json()
        email = data['email']
        user = User.query.filter_by(email=email).first()
        # db.session.commit()
        if user:
            if user.is_deleted == True:
                return jsonify({'status': 0, 'message': 'This account is deleted'})
        
        if not user:
            return jsonify({'status':0, 'message': 'User does not exist !'})
        
        elif user and user.is_block==True:
            return jsonify(
                {'status': 0, 'message': 'User is blocked'})

        elif user  and user.is_block==0:
            send_reset_email(user)
            return jsonify({'status': 1, 'message': 'Reset Link has been send to your gmail'})

@user_auth.route('/user/user_reset_password/<token>',methods=['GET', 'POST'])
def user_reset_token(token):
    return render_template('forget_password.html',token=token,common_path=common_path)

@user_auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_token(token)
    if user is None:
        return 'Invalid or Expired Token'

    if user and request.method == 'POST':

        new_password = request.form.get('password')

        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            hash_password = generate_password_hash(new_password)
            user.password = hash_password
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_auth.success"))
        else:
            flash('Password  does not match , Try Again.. ','danger')
            return redirect(url_for('user_auth.user_reset_token', token=token))
        
@user_auth.route("/success", methods=['GET', 'POST'])
def success():
    return render_template('Success_msg.html',common_path=common_path)

@user_auth.route('/user/update_profile', methods=['POST'])
@token_required
def user_update(active_user):
    token=request.headers.get('Authorization')
    print(token)
    email= request.form.get("email")
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':

        if active_user:
            if active_user.is_deleted == True:
                return jsonify({'status': 0, 'message': 'This account is deleted'})

        if active_user and active_user.is_block==1:
            return jsonify({'status': 0, 'message': 'User is blocked'})

        elif  user and user.email!=active_user.email:
            return jsonify({'status': 0, 'message': 'email is already taken'})

        elif active_user and active_user.is_block==0:
            if request.files :

                form_picture = request.files.get('profile_pic')

                if active_user.image_name != 'default.png':
                    os.remove(os.path.join(UPLOAD_FOLDER,  active_user.image_name))
                image_name = secure_filename(form_picture.filename)
                extension = os.path.splitext(image_name)[1]
                x = secrets.token_hex(10)
                picture_fn = x + extension
                print(picture_fn)
                form_picture.save(os.path.join(UPLOAD_FOLDER, picture_fn))
                active_user.image_name = picture_fn
                
            active_user.fullname = request.form.get('fullname')
            active_user.username = request.form.get('username')
            active_user.email = request.form.get('email')
            active_user.discord_link= request.form.get('discord_link')
            db.session.commit()

            return jsonify({'status': 1, 'message': 'Sucessfully Updated Profile', 'data': active_user.user_data(token=token)})
        else:
            return jsonify({'status': 0, 'message': 'Invalid Token'})