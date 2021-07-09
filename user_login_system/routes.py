import os
import secrets

from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from user_login_system import app, db, bcrypt, mail
from user_login_system.forms import (RegisterationForm, LoginForm, UpdateAccountForm, AccountVerificationForm,
                                     RequestResetForm, ResetPasswordForm)
from user_login_system.models import User


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.username != 'admin').paginate(per_page=5, page=page)
    admins = User.query.filter(User.username == 'admin')
    return render_template("about.html", title='About', users=users, admins=admins)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        print('form validated')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Registeration successful. You can login now.', 'success')
        return redirect(url_for('login'))
    # else:
    #     print('Validation failed! with errors: ', form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        print('Form validation successful!!!')
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login Successful. Welcome {user.username}', 'success')
            next_page = request.args.get('next')
            if next_page:
                if user.email == 'admin@demo.com':
                    return redirect(url_for('admin_panel'))
                return redirect(url_for('user_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login Failed. Please check your email and password!', 'danger')
    # else:
    #     print('Validation failed!!!')
    #     print(form.errors)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/adminpanel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.username != 'admin').paginate(per_page=5, page=page)
    # users = User.query.filter(User.username != 'admin').filter(User.reviewed == False).all()
    # admin profile pic
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('admin_panel.html', title='Admin Panel', users=users, profile_pic=profile_pic)


def save_picture(profile_pic):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(profile_pic.filename)
    new_profile_pic = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', new_profile_pic)

    output_size = (125, 125)
    i = Image.open(profile_pic)
    i.thumbnail(output_size)
    i.save(pic_path)

    return new_profile_pic


@app.route('/userdashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    if current_user.is_authenticated:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.profile_pic.data:
                pic_file = save_picture(form.profile_pic.data)
                old_pic_data = current_user.profile_pic
                current_user.profile_pic = pic_file
                old_path = os.path.join(app.root_path, 'static/profile_pics', old_pic_data)
                # if old_pic_data != 'default.jpg':
                #     os.remove(old_path)
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your Account has been updated.', 'success')
            return redirect(url_for('user_dashboard'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
        return render_template('user_dashboard.html', title='User Dashboard', profile_pic=profile_pic, form=form)


# This route will be used by admin to approve or delete users
@app.route('/userVerification/<string:username>', methods=['GET', 'POST'])
@login_required
def user_verification(username):
    user = User.query.filter(User.username == username).first()
    profile_pic = url_for('static', filename='profile_pics/' + user.profile_pic)
    # print(user, '\n')
    if user.username != 'admin':
        form = AccountVerificationForm()
        if form.is_submitted():
            if form.delete.data:
                # delete account
                db.session.delete(user)
                flash('User account has been deleted!', 'success')
            else:
                if form.verify.data:
                    # set verify to True
                    user.is_verified = True
                user.reviewed = True
                flash(f'User Verification process for {user.username} finished.', 'success')
            db.session.commit()
            return redirect(url_for('admin_panel'))
        else:
            print(f'\nForm Errors: {form.errors}\n')
        return render_template('user_verification.html', title='User Verification', form=form, user=user,
                               profile_pic=profile_pic)
    else:
        return redirect(url_for('home'))


def send_reset_password_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""
To reset your password please click on the link below:

{url_for('reset_password', token=token, _external=True)}

If you did not made this request, please ignore this mail.
"""
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password_email(user)
        flash('Please check your email for instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This token is either invalid or has expired!!!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated. Please login!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
