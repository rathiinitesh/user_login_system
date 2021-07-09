# user_login_system
User login system with an admin overseeing eveything.

Requirements for the app :-

For getting this app to work, please add environment variables for secret key, database uri, 
email username and password.

For creating secret key use secrets module >> token_hex method.

variable_name: 'ULS_DATABASE_URI', variable_value = 'sqlite:///users.db'

Right now, the server being used is googlemail, please do make sure that the email account mentioned 
below is a gmail account else, go to the __init__.py file of package user_login_system and change the 
app config key for mail_server.

key: 'MAIL_SERVER'

Email id for sending emails for resetting password i.e. emails will be sent by this account:

variable_name: 'EMAIL_USERNAME', variable_value = 'example@gmail.com'

Password for the above account:

variable_name: 'EMAIL_PASSWORD', variable_value = 'password'.

Now, run requirements.txt file. It contains all the libraries and modules necessary for the app to work.

"pip install -r requirements.txt"


# Now, we are ready to launch the app.

Run app.py file.

Register as a user.

Admin account already exists.
        email: "admin@demo.com"
        password: "admin"
 
Feel, free to experiment.

Enjoy!!!
