# user_login_system
User login system with an admin overseeing eveything.

Requirements for the app :-

For getting this app to work, please set environment variables for secret key, database uri, 
email username and password.

For Linux/Mac:
    In .bash.profile : 
        export varible_name=variable_value
    In windows : 
        Control Panel >> System and Security >> System >> System Properties/Allow remote access >> 
        Advanced >> Environment Variables >> User variables >> New >> Variable name and value.
        
         
For creating secret key use secrets module >> token_hex method.

For Database: 

variable_name: 'ULS_DATABASE_URI', variable_value = 'sqlite:///users.db'

Right now, the mail server being used is googlemail, please do make sure that the email account mentioned 
below is a gmail account else, go to the config.py file of package user_login_system and change the 
'MAIL_SERVER' variable value.

key: 'MAIL_SERVER'

Email id for sending emails for resetting password i.e. account that will be used for sending reset link:

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
 
App also has some custom error handler routes for errors like 403, 404, 500.
For testing one try going to a page that does not exist like in url bar of your browser 
enter """locahost:5000/test"""
You will recieve a nice custom 404 error page instead of default nasty one.

Now, feel free to experiment.

Enjoy!!!
