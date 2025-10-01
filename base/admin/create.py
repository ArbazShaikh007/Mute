from flask import Blueprint, render_template, request, flash, redirect, url_for
from base.database.db import db
from flask_login import login_required, current_user
from base.api.user.models import MindSubCategory,Mind, Reflect, Listen,User
from base.admin.models import Category, Exercise
from base.admin.queryset import insert_data, save, delete_record
import os
from werkzeug.security import secrets
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime
import requests
import json
from base.common.utils import common_path

admin_create = Blueprint('admin_create', __name__)
EXERCISE_IMAGE = 'base/static/exercise_image/'

AUDIO_FOLDER = "base/static/audio/"

# BODY category

@admin_create.route('/admin/add_category',methods=['GET','POST'])
@login_required
def add_category():
    if request.method=='POST':
        cat_name=request.form.get('cat_name')
        cat=Category(cat_name=cat_name)
        insert_data(cat)
        flash("category added successfully",'success')
        return redirect(url_for('admin_view.category_page'))

@admin_create.route('/admin/add_category/<int:cat_id>/edit_category',methods=['GET','POST'])
@login_required
def edit_category(cat_id):
    if request.method=='POST':
        cat_name=Category.query.get(cat_id)
        cat_name.cat_name=request.form.get('cat_name')
        save()
        flash("category updated successfully","success")
        return redirect(url_for('admin_view.category_page'))
        
@admin_create.route('/admin/add_category/<int:cat_id>/delete_category',methods=['GET','POST'])
@login_required
def delete_category(cat_id):
    if request.method=='POST':
        cat_name=Category.query.get(cat_id)
        delete_record(cat_name)
        flash('category deleted successfully','success')
        return redirect(url_for('admin_view.category_page'))

def save_audio(exercise_audio):

    random_hex=secrets.token_hex(8)
    _,f_ext = os.path.splitext(exercise_audio.filename)
    picture_fn=random_hex + f_ext
    audio_path = os.path.join(AUDIO_FOLDER, picture_fn)
    exercise_audio.save(audio_path)

    return picture_fn

def save_picture(form_picture):
    # if current_user.image_file !="default.jpg":
    #     os.remove(os.path.join(EXERCISE_IMAGE,current_user.image_file))
    random_hex=secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path = os.path.join(EXERCISE_IMAGE,picture_fn)
    i=Image.open(form_picture)
    i = i.resize((500, 500))
    i.save(picture_path)

    return picture_fn

@admin_create.route("/admin/body/<int:cat_id>/add_exercise", methods=['GET', 'POST'])
@login_required
def add_exercise(cat_id):
    if request.method == "POST":
        title = request.form.get('exercise_name')
        description = request.form.get('description')

        # Collect dynamic tag fields: tags, tags1, tags2, ...
        tags = []
        for i in range(10):  # support up to 10 tags
            name = "tags" if i == 0 else f"tags{i}"
            val = request.form.get(name, "").strip()
            if val:
                if not val.startswith("#"):
                    val = f"#{val}"
                tags.append(val)

        tag_str = ",".join(tags)

        # Save files
        image_files = save_picture(request.files.get('image'))
        audio_file = request.files.get('audio')
        audio = save_audio(audio_file) if audio_file and audio_file.filename else None

        # Create exercise
        exercise = Exercise(
            title=title,
            description=description,
            tags=tag_str,
            image_file=image_files,
            audio_file=audio,
            created_at=datetime.utcnow(),
            cat_id=cat_id
        )
        db.session.add(exercise)
        db.session.commit()

        flash('Exercise added successfully', 'success')
        return redirect(url_for('admin_view.exercise_page', cat_id=cat_id))

    return render_template('add_body_exercise.html', cat_id=cat_id, common_path=common_path)

@admin_create.route("/admin/body/<int:cat_id>/edit_exercise/<int:exercise_id>", methods=['GET', 'POST'])
@login_required
def edit_exercise(cat_id, exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)

    if request.method == "POST":
        exercise.title = request.form.get('exercise_name')
        exercise.description = request.form.get('description')

        # Update image if provided
        image = request.files.get('image')
        if image and image.filename:
            exercise.image_file = save_picture(image)

        # Update audio if provided
        audio_file = request.files.get('audio')
        if audio_file and audio_file.filename:
            exercise.audio_file = save_audio(audio_file)

        # Tags (split by comma or spaces)
        raw_tags = request.form.get('tags', "")
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
        clean_tags = []
        for tag in tags:
            if not tag.startswith("#"):
                tag = f"#{tag}"
            clean_tags.append(tag)
        exercise.tags = ",".join(clean_tags)

        db.session.commit()

        flash('Exercise updated successfully', 'success')
        return redirect(url_for('admin_view.body_page_detail',
                                cat_id=cat_id, exercise_id=exercise.id))

    return render_template('body_excercise_detail.html',
                           cat_id=cat_id, exercises=exercise,
                           common_path=common_path)

@admin_create.route('/admin/body/<int:exe_id>/delete_exercise', methods=['POST'])
@login_required
def delete_exercise(exe_id):
    my_exe = Exercise.query.get_or_404(exe_id)
    cat_id = my_exe.cat_id
    db.session.delete(my_exe)
    db.session.commit()
    flash('Exercise deleted successfully', 'success')
    return redirect(url_for('admin_view.exercise_page', cat_id=cat_id))

# MIND Category 

#1 Mind's Reflect category

@admin_create.route('/admin/add_mind_category',methods=['GET','POST'])
@login_required
def add_mind_category():
    if request.method=='POST':
        sub_cat=request.form.get('sub_cat')
        mind=Mind(sub_cat=sub_cat, created_at=datetime.utcnow())        
        insert_data(mind)
        flash("category added successfully",'success')

        return redirect(url_for('admin_view.mind_category_page'))

@admin_create.route('/admin/mind_review_category',methods=['GET','POST'])
@login_required
def mind_review_category():
    if request.method=='POST':
        sub_cat=request.form.get('sub_cat')
        mind=Mind(sub_cat=sub_cat, created_at=datetime.utcnow())        
        insert_data(mind)
        flash("category added successfully",'success')

        return redirect(url_for('admin_view.review_mind_category_page'))

@admin_create.route('/admin/add_mind_category/<int:mind_id>/delete_mind_category',methods=['GET','POST'])
@login_required
def delete_mind_category(mind_id):
    if request.method=='POST':
        sub_cat=Mind.query.get(mind_id)
        delete_record(sub_cat)
        flash('category deleted successfully','success')
        return redirect(url_for('admin_view.mind_category_page',mind_id=mind_id))

# @admin_create.route('/admin/add_mind_category/<int:cat_id>/edit_mind_category',methods=['GET','POST'])
# @login_required
# def edit_mind_category(cat_id):
#     if request.method=='POST':
#         sub_cat=Mind.query.get(cat_id)
#         sub_cat.sub_cat=request.form.get('sub_cat')
#         save()
#         flash("Mind category updated successfully","success")
#         return redirect(url_for('admin_view.mind_category_page'))

@admin_create.route('/admin/add_mind_category/<int:mind_id>/delete_reflect_category',methods=['GET','POST'])
@login_required
def delete_reflect_category(mind_id):
    if request.method=='POST':
        sub_cat=Reflect.query.get(mind_id)
        delete_record(sub_cat)
        flash('category deleted successfully','success')
        return redirect(url_for('admin_view.mind_reflect_page',mind_id=sub_cat.mind_id))

@admin_create.route('/admin/reflect/<int:mind_id>/approve',methods=['GET','POST'])
@login_required
def approve_reflect(mind_id):
    if request.method=='POST':
        # reflect=Reflect.query.get(mind_id)

        reflect = MindSubCategory.query.get(mind_id)

        reflect.admin_review_status = 'approved'
        db.session.commit()
        push_notification(deviceToken=reflect.user.device_id,title='post approved',msg="your content has been approved.")

        flash('Reflect post approved successfully','success')
        return redirect(url_for('admin_view.review_reflect_post',mind_id=reflect.mind_id))

@admin_create.route('/admin/reflect/<int:mind_id>/reject',methods=['GET','POST'])
@login_required
def reject_reflect(mind_id):
    if request.method=='POST':
        # reflect=Reflect.query.get(mind_id)

        reflect = MindSubCategory.query.get(mind_id)

        user = User.query.get(reflect.user_id)
        reflect.admin_review_status = 'rejected'
        reflect.reject_reason = request.form.get('message')

        db.session.commit()

        push_notification(deviceToken=user.device_id,title='post rejected',msg=request.form.get('message'))

        flash('Reflect post rejected successfully','success')
        return redirect(url_for('admin_view.review_reflect_post',mind_id=reflect.mind_id))

#2 Mind's Listen category

@admin_create.route('/admin/add_mind_category/<int:mind_id>/delete_listen_category',methods=['GET','POST'])
@login_required
def delete_listen_category(mind_id):
    if request.method=='POST':
        # sub_cat=Listen.query.get(mind_id)
        sub_cat = MindSubCategory.query.get(mind_id)

        delete_record(sub_cat)
        flash('category deleted successfully','success')
        return redirect(url_for('admin_view.mind_listen_page',mind_id=sub_cat.mind_id))

@admin_create.route('/admin/listen/<int:mind_id>/approve',methods=['GET','POST'])
@login_required
def approve_listen(mind_id):
    if request.method=='POST':
        # listen=Listen.query.get(mind_id)
        print('mind_id',mind_id)
        listen = MindSubCategory.query.get(mind_id)

        listen.admin_review_status = 'approved'
        db.session.commit()
        push_notification(deviceToken=listen.user.device_id,title='post approved',msg="your content has been approved.")
        flash('Listen post approved successfully','success')
        return redirect(url_for('admin_view.review_listen_post',mind_id=listen.mind_id))

@admin_create.route('/admin/listen/<int:mind_id>/reject',methods=['GET','POST'])
@login_required
def reject_listen(mind_id):
    if request.method=='POST':
        # listen=Listen.query.get(mind_id)

        listen = MindSubCategory.query.get(mind_id)

        user = User.query.get(listen.user_id)

        listen.admin_review_status = 'rejected'
        listen.reject_reason = request.form.get('message')

        db.session.commit()

        push_notification(deviceToken=user.device_id,title='post rejected',msg=request.form.get('message'))

        flash('Listen post rejected successfully','success')
        return redirect(url_for('admin_view.review_listen_post',mind_id=listen.mind_id))

def push_notification(deviceToken,title,msg):
    serverToken  = 'AAAAMGhEHxE:APA91bHclxPektg9Pmffo9hhCtZ6usqookOfyJ30FY00tEzTXZ5C-OBEKuKYje2a-7IOQzdoMPElubHX9JbZGEhRtQgiWOjVuIShqyFEobmyRmFo1eGZIm99tqLCxnLPr3wUD8P_q_3C'

    headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }
    body = {
                'notification': {'title': title,
                                    'body': msg
                                    },
                'to':
                    deviceToken,
                'priority': 'high',
                }
    response=requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))

    return response

@admin_create.route("/admin/push_notification",methods=['GET','POST'])
def admin_push_notification():
    if request.method=="POST":
        users =  User.query.all()
        title = request.form.get('title')
        msg = request.form.get('body')
        for i in users :
            notification=push_notification(deviceToken=i.device_id, title=title, msg=msg)
           
        flash("notification pushed successfully",'success')
        return redirect(url_for('admin_create.admin_push_notification',notification=notification))
    
    return render_template('push_notification.html',is_active='push_notification',common_path=common_path)