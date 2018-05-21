import app


class GlobalUser():
    username = "flaskuser"
    password = app.bcrypt.generate_password_hash("flask")


