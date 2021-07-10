import os
import secrets

from PIL import Image
from flask import url_for
from flask_mail import Message

from user_login_system import app, mail


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


def send_reset_password_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""
To reset your password please click on the link below:

{url_for('users.reset_password', token=token, _external=True)}

If you did not made this request, please ignore this mail.
"""
    mail.send(msg)
