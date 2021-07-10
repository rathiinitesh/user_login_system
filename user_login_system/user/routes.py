from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user

from user_login_system import bcrypt, db
from user_login_system.models import User
from user_login_system.user.forms import (RegisterationForm, LoginForm, UpdateAccountForm, AccountVerificationForm,
                                          RequestResetForm, ResetPasswordForm)
from user_login_system.user.utils import save_picture, send_reset_password_email

users = Blueprint('users', __name__)


# Route for a new user to register
@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        print('form validated')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Registeration successful. You can login now.', 'success')
        return redirect(url_for('users.login'))
    # else:
    #     print('Validation failed! with errors: ', form.errors)
    return render_template('register.html', title='Register', form=form)


# Route for a registered user to login
@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        print('Form validation successful!!!')
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_verified or not user.reviewed:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                if user.reviewed:
                    flash(f'Login Successful. Welcome {user.username}', 'success')
                else:
                    flash(f'Login Successful. Welcome {user.username}. This account is still up for review.', 'success')
                next_page = request.args.get('next')
                if next_page:
                    if user.email == 'admin@demo.com':
                        return redirect(url_for('users.admin_panel'))
                    return redirect(url_for('users.user_dashboard'))
                else:
                    return redirect(url_for('main.home'))
            else:
                flash(f'Login Failed. Please check your email and password!', 'danger')
        else:
            flash('Login not possible. Your account has been disapproved by admin!', 'danger')
            return redirect(url_for('main.home'))
    # else:
    #     print('Validation failed!!!')
    #     print(form.errors)
    return render_template('login.html', title='Login', form=form)


# Route for a logged in user to logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Route for admin to look into all the non-verified users
@users.route('/adminpanel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.username == 'admin':
        page = request.args.get('page', 1, type=int)
        users = User.query.filter(User.username != 'admin').filter(User.reviewed == False)\
            .paginate(per_page=5, page=page)
        # users = User.query.filter(User.username != 'admin').filter(User.reviewed == False).all()
        # admin profile pic
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
        return render_template('admin_panel.html', title='Admin Panel', users=users, profile_pic=profile_pic)
    else:
        flash(f'You are not an admin. This page is not accessible to you.', 'danger')
        return redirect(url_for('users.user_dashboard'))


@users.route('/userdashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    if current_user.username != 'admin':
        form = UpdateAccountForm()
        if form.validate_on_submit():
            old_pic_data = current_user.profile_pic
            # old_path = os.path.join(app.root_path, 'static/profile_pics', old_pic_data)
            if form.profile_pic.data and not form.delete.data:
                pic_file = save_picture(form.profile_pic.data)
                current_user.profile_pic = pic_file
                # if old_pic_data != 'default.jpg':
                #     os.remove(old_path)

            if form.delete.data and current_user.profile_pic != 'default.jpg':
                # os.remove(old_path)
                current_user.profile_pic = 'default.jpg'
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            if form.delete.data and old_pic_data == 'default.jpg':
                flash(f'It will take all your might to delete this default profile image or just delete it directly '
                      f'from the folder that will do the trick.', 'success')
            else:
                flash('Your Account has been updated.', 'success')
            return redirect(url_for('users.user_dashboard'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
        return render_template('user_dashboard.html', title='User Dashboard', profile_pic=profile_pic, form=form)
    else:
        flash('You are an admin, act as one!', 'danger')
        return redirect(url_for('users.admin_panel'))


# This route will be used by admin to approve or delete users
@users.route('/userVerification/<string:username>', methods=['GET', 'POST'])
@login_required
def user_verification(username):
    user = User.query.filter(User.username == username).first()
    profile_pic = url_for('static', filename='profile_pics/' + user.profile_pic)
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
            return redirect(url_for('users.admin_panel'))
        # else:
        #     print(f'\nForm Errors: {form.errors}\n')
        return render_template('user_verification.html', title='User Verification', form=form, user=user,
                               profile_pic=profile_pic)
    else:
        return redirect(url_for('main.home'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password_email(user)
        flash('Please check your email for instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This token is either invalid or has expired!!!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated. Please login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
