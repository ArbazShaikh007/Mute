from flask import request, flash, redirect, render_template, url_for, Blueprint
from base.admin.queryset import  get_user, insert_data, save
from flask_login import login_user, logout_user, current_user, login_required
from base.admin.models import Admin, Terms, Privacy
from base.api.user.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os, secrets, datetime
from PIL import Image
from base.admin.utils import send_reset_email
from base.database.db import db
from base.common.utils import common_path

ADMIN_PROFILE = 'base/static/admin_profile/'

admin_auth = Blueprint('admin_auth', __name__)

@admin_auth.route("/admin/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        hashed_password = generate_password_hash(request.form.get('password-input'))

        admin= get_user(email)
        if admin :
            flash('Email  is already Taken','danger')
        else :
            admin = Admin(fname=fname,lname=lname,email=email,password=hashed_password,image_file="default.jpg",created_at=datetime.datetime.utcnow())
            insert_data(admin)
            login_user(admin)
            flash('Your account has been created successfully!', 'success')
            return redirect(url_for('admin_view.home'))
 
    return render_template('register.html',title="Register",common_path=common_path)

@admin_auth.route("/",methods=['GET','POST'])
@admin_auth.route("/admin/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        user = get_user(request.form.get('email'))
        if user and check_password_hash(user.password, request.form.get('password-input')) :
            login_user(user) 
            flash('Login Successful','success')
            return redirect(url_for('admin_view.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',title="Login",common_path=common_path)

@admin_auth.route("/admin/logout")
def logout():
    logout_user()
    flash('Logout successful ', 'success')

    return redirect(url_for('admin_auth.login'))

def save_picture(form_picture):
    # if current_user.image_file !="default.jpg":
    #     os.remove(os.path.join(ADMIN_PROFILE,current_user.image_file))
    random_hex=secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path = os.path.join(ADMIN_PROFILE,picture_fn)
    i=Image.open(form_picture)
    i = i.resize((500,500))
    i.save(picture_path)

    return picture_fn

@admin_auth.route("/admin/user_profile",methods=['GET','POST'])
@login_required
def user_profile():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    return render_template('pages-profile.html',title="User Profile",page_name='User Profile', is_active='user_profile',common_path=common_path)

@admin_auth.route("/admin/update_profile",methods=['GET','POST'])
@login_required
def update_profile():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    
    elif request.method == "POST":
        user=get_user(request.form.get('email'))
        profile_pic = request.files.get('profile_pic')
        if user and user.email!= current_user.email: 
         flash('Email is already taken ','danger')
        else :
            if profile_pic:
                        picture_file = save_picture(request.files.get('profile_pic'))
                        current_user.image_file = picture_file
            current_user.fname=request.form.get('fname')
            current_user.lname=request.form.get('lname')
            current_user.phone=request.form.get('phone')
            current_user.email=request.form.get('email')
            save()
            flash('Profile updated successfully !','success')
            return redirect(url_for('admin_auth.user_profile'))

    return render_template('pages-profile-settings.html',title="Edit Profile" ,page_name='Edit Profile', is_active='edit_profile',common_path=common_path)

@admin_auth.route("/admin/change_password", methods=['GET','POST'])
@login_required
def change_password():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    elif request.method=='POST' :
          if check_password_hash(current_user.password, request.form.get('old_pass')) == False:
                    flash('Wrong Password','danger')
                    return redirect(url_for('admin_auth.update_profile'))
          elif check_password_hash(current_user.password, request.form.get('password')) == True:
                   flash("New password can't be same as old Password ",'danger')
                   return redirect(url_for('admin_auth.update_profile'))
          elif check_password_hash(current_user.password, request.form.get('old_pass')) == True:
               hashed_password = generate_password_hash(request.form.get('password'))
               current_user.password = hashed_password 
               save()
               flash("Password Changed SuccessFully ",'success')
               return redirect(url_for('admin_auth.user_profile'))

@admin_auth.route("/Block/<int:user_id>", methods=['GET', 'POST'])
def block_user(user_id):
    user= User.query.get(user_id)
    if user.is_block == False:
        user.is_block = True
        save()
        flash(f'{user.username} is Blocked !!', 'success')
        return redirect(url_for('admin_view.total_users'))
    else :
        user.is_block = False
        save()
        flash(f'{user.username} is Unblocked !!', 'success')
        return redirect(url_for('admin_view.total_users'))

@admin_auth.route("/admin/terms",methods=['GET','POST'])
@login_required
def terms():
    my_content = Terms.query.first()
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    elif request.method=="POST":
        if my_content:
            my_content.content= request.form.get("content")
            save()
        else :
            term =Terms(content=request.form.get("content"),created_at=datetime.datetime.utcnow())
            insert_data(term)

    return render_template('terms_n_condition.html',content=my_content,title="Terms & Conditions",page_name='Terms & Condition' , is_active='terms',common_path=common_path)

@admin_auth.route("/admin/privacy_policy",methods=['GET','POST'])
@login_required
def privacy_policy():
    my_content = Privacy.query.first()
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    elif request.method=="POST":
        if my_content:
            my_content.content = request.form.get("body")
            save()
        else :
            term = Privacy(content=request.form.get("body"),created_at=datetime.datetime.utcnow())
            insert_data(term)
            save()

    return render_template('privacy_n_policy.html',content=my_content,title="Privacy & Policy" ,page_name='Privacy Policy', is_active="privacy",common_path=common_path)

@admin_auth.route("/reset_request", methods=['GET','POST'])
def reset_request():
    
    if request.method=="POST":
        user = get_user(request.form.get('email'))
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('admin_auth.login'))

    return render_template('reset_request.html', title="Forget Password", page_name='Reset Request',common_path=common_path)

@admin_auth.route("/admin/reset_token/<token>", methods=['GET', 'POST'])
def reset_token(token):
    return render_template('reset_admin_password.html', title='Reset Password',token=token,common_path=common_path)

@admin_auth.route('/admin/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = Admin.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('admin_auth.reset_request'))
    elif request.method=='POST' :
        hashed_password = generate_password_hash(request.form.get('password'))
        user.password = hashed_password
        save()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('admin_auth.success'))

@admin_auth.route("/success", methods=['GET', 'POST'])
def success():
    return render_template('success_msg.html',common_path=common_path)

@admin_auth.before_request
def check_authenticated():
    if current_user.is_authenticated and request.endpoint == 'admin_auth.login':
        logout_user()
        flash('You have been automatically logged out. Please log in again.', 'warning')

@admin_auth.before_request
def check_authenticated():
    if current_user.is_authenticated and request.endpoint == 'admin_auth.login':
        logout_user()
        flash('You have been automatically logged out. Please log in again.', 'warning')