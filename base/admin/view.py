from flask import Blueprint, render_template, url_for, redirect, flash, request
from base.admin.queryset import total_user_count, all_users, mind_count, total_session, total_review_category, total_feedback
from flask_login import login_required, current_user, logout_user
from base.admin.models import Terms, Privacy, Category, Exercise
from base.api.user.models import MindSubCategory,Contact_us, Mind, Reflect, Listen, Session, Feedback
from base.database.db import db
from base.common.utils import common_path

admin_view = Blueprint('admin_view', __name__)

@admin_view.route('/home')
def home():
    if current_user.is_anonymous:
        return redirect(url_for('admin_auth.login'))
    users = total_user_count()
    mind = mind_count()
    session=total_session()
    feeds=total_feedback()
    category = len(Category.query.all())
    review_cat=total_review_category()
    return render_template('index.html',users=users, category=category,title="Home",session=session,feeds=feeds,review_cat=review_cat,mind=mind,page_name='Dashboard',is_active='home',common_path=common_path)

@admin_view.route("/total_users", methods=['GET', 'POST'])
@login_required
def total_users():
    if  current_user.is_anonymous:
        flash("first login to access this page","info")
        return redirect(url_for('admin_auth.login'))
    else :
        users = all_users()
        
    return render_template('total_user.html',users=users,Title="Total Users", page_name='Total Users',is_active='total_users',common_path=common_path)

@admin_view.route("/admin/display_terms", methods=['GET','POST'])
def display_terms():
    content = Terms.query.first()
    return render_template('display_terms.html', content=content,page_name='Terms & Condition',is_active='terms',common_path=common_path)

@admin_view.route("/admin/display_privacy", methods=['GET','POST'])
def display_policy():
    content = Privacy.query.first()

    return render_template('display_privacy.html', content=content,page_name='Privacy Policy',is_active='privacy',common_path=common_path)

@admin_view.route("/admin/contact_page", methods=['GET','POST'])
def contact_page():
    contact_us=Contact_us.query.all()
    return render_template('contact_page.html',page_name='contact_us',is_active='contact_us',title="contact_us", page="resources",contact_us=contact_us,common_path=common_path)

@admin_view.route("/admin/<int:contact_id>/contact_us_message", methods=['GET','POST'])
def contact_us_message(contact_id):
    contact_message=Contact_us.query.get(contact_id)
    if contact_message.read==False:
       contact_message.read=True
       db.session.commit()

    return render_template('contact_us_messages.html',page_name='contact_us',is_active='contact_us',title="contact_us", page="resources",contact_message=contact_message,common_path=common_path)

@admin_view.route("/admin/feedback_page", methods=['GET','POST'])
def feedback_page():
    feedbacks=Feedback.query.all()
    return render_template('feedback_page.html',page_name='feedback',is_active='feedback',title="feedback", page="feedback_page",feedbacks=feedbacks,common_path=common_path)

@admin_view.route("/admin/<int:feedback_id>/feedback_message", methods=['GET','POST'])
def feedback_message(feedback_id):
    feedback_message=Feedback.query.get(feedback_id)
    if feedback_message.read==False:
       feedback_message.read=True
       db.session.commit()

    return render_template('feedback_message.html',page_name='feedback',is_active='feedback',title="feedback", page="feedback",feedback_message=feedback_message,common_path=common_path)

@admin_view.route("/admin/category_page", methods=['GET','POST'])
def category_page():
    categories=Category.query.all()
    return render_template('add_body_category.html',page_name='category',is_active='category',title="category", page="resources",categories=categories,common_path=common_path)

# def get_image(exercise_id):
#     return Exercise_mul_image.query.filter_by(exercise_id=exercise_id).all()

def get_tags(execise_id):
    exercise = Exercise.query.get(execise_id)
    tags = exercise.tags
    tags=tags.split(",")
    for i in tags :
        if i == '':
            tags.remove(i)

    return tags

@admin_view.route("/admin/<int:cat_id>/exercise_page", methods=['GET','POST'])
def exercise_page(cat_id):
    exercises=Exercise.query.filter_by(cat_id=cat_id).all()
    return render_template('add_body_exercise.html',page_name='Body_exercise',is_active='category',title="exercise", page="exercise",exercises=exercises,cat_id=cat_id,get_tags=get_tags,common_path=common_path)

@admin_view.route("/admin/<int:cat_id>/<int:exercise_id>/body_page_detail", methods=['GET','POST'])
def body_page_detail(cat_id,exercise_id):
    exercises=Exercise.query.filter_by(id=exercise_id).first()
    return render_template('body_excercise_detail.html',page_name='Body',is_active='body',title="exercise", page="Body Exercise",exercises=exercises,cat_id=cat_id,get_tags=get_tags,common_path=common_path,exercise_id=exercise_id)

@admin_view.route("/admin/mind_category_page", methods=['GET','POST'])
def mind_category_page():
    minds=Mind.query.all()
    return render_template('add_mind_category.html',page_name='mind_category',is_active='mind_category',title="mind_category", page="mind_category",minds=minds,common_path=common_path)

@admin_view.route("/admin/<int:mind_id>/mind_reflect_page", methods=['GET','POST'])
def mind_reflect_page(mind_id):
    # mind_exercises=Reflect.query.filter_by(mind_id=mind_id).all()
    mind_exercises = MindSubCategory.query.filter_by(mind_id=mind_id).all()

    return render_template('add_mind_reflect_exercise.html',page_name='mind_reflect',is_active='mind_category',title="exercise", page="exercise",mind_exercises=mind_exercises,mind_id=mind_id,common_path=common_path)

# @admin_view.route("/admin/<int:mind_id>/admin_mind_listen_page", methods=['GET','POST'])
# def admin_mind_listen_page(mind_id):
#     admin_listen_exercises=Listen.query.filter_by(mind_id=mind_id).all()
#     return render_template('admin_mind.html',page_name='Mind_listen',is_active='mind_category',title="exercise", page="exercise",admin_listen_exercises=admin_listen_exercises,mind_id=mind_id,common_path=common_path)

@admin_view.route("/admin/<int:mind_id>/mind_listen_page", methods=['GET','POST'])
def mind_listen_page(mind_id):

    # mind_listen_exercises=Listen.query.filter_by(mind_id=mind_id).all()
    mind_listen_exercises = MindSubCategory.query.filter_by(mind_id=mind_id).all()

    return render_template('add_mind_listen_exercise.html',page_name='Mind_listen',is_active='mind_category',title="exercise", page="exercise",mind_listen_exercises=mind_listen_exercises,mind_id=mind_id,common_path=common_path)

@admin_view.route("/admin/status_category", methods=['GET','POST'])
def status_category():
    statuses=Session.query.all()
    return render_template('add_status_category.html',page_name='status_category',is_active='Session',title="status_category", page="mind_category",statuses=statuses,common_path=common_path)

@admin_view.route("/admin/review_mind_category_page", methods=['GET','POST'])
def review_mind_category_page():
    minds=Mind.query.all()

    listen_id = 0
    reflect_id = 0

    if len(minds)>0:
        for i in minds:
            if i.sub_cat == "Listen":
                listen_id = i.id
            elif i.sub_cat == "Reflect":
                reflect_id = i.id

    return render_template('review_category.html',listen_id=listen_id,reflect_id=reflect_id,page_name='mind_category',is_active='status_category',title="mind_category", page="mind_category",minds=minds,common_path=common_path)

@admin_view.route("/admin/review_reflect_post", methods=['GET','POST'])
def review_reflect_post():
    # mind_exercises  = Reflect.query.filter_by(admin_review_status="under_review").all()

    mind_exercises = MindSubCategory.query.filter_by(admin_review_status="under_review",type="Reflect").all()

    return render_template('review_reflect.html',mind_exercises=mind_exercises,is_active='status_category',common_path=common_path)

@admin_view.route("/admin/review_listen_post", methods=['GET','POST'])
def review_listen_post():
    # mind_listen_exercises  = Listen.query.filter_by(admin_review_status="under_review").all()

    mind_listen_exercises = MindSubCategory.query.filter_by(admin_review_status="under_review",type="Listen").all()

    return render_template('review_listen.html',mind_listen_exercises=mind_listen_exercises,is_active='status_category',common_path=common_path)

@admin_view.before_request
def check_authenticated():
    if current_user.is_authenticated and request.endpoint == 'admin_auth.login':
        logout_user()
        
        flash('You have been automatically logged out. Please log in again.', 'warning')