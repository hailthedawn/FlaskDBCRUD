from flask import render_template, redirect, request, url_for
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
#import PasswordEncrypt
#from PasswordEncrypt import GlobalUser

app=Flask(__name__)

#globalUser = GlobalUser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskuser:flask@12345@localhost/students'
#app.config(SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" + globalUser.username + ":" + globalUser.password + "@127.0.0.1:54990/students")
db = SQLAlchemy(app)                                #
db.session.commit()


class Student(db.Model):

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(64), unique=True)
    stu_course = db.Column('stu_course', db.String(64))

    def __init__(self, name, stu_course):
       # self.id=id
        self.name = name
        self.stu_course = stu_course

    def __repr__(self):
        return '<Student {}:{}>'.format(self.name, self.stu_course)

db.drop_all()
db.create_all()

@app.route('/', methods=['GET'])
def home():
    #TODO use JSON
    examples = Student.query.all()
    return render_template("students.html", rows=examples)


@app.route('/add-student', methods=['POST'])
def post_student():
    new_student = Student(request.form['name'], request.form['stu_course'])   #TODO without passing primary key
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.__repr__())


#@app.route('/update-student', methods=['POST'])
#def update_student():


@app.route('/remove-student', methods=['POST'])
def remove_student():
    print("Here")
    new_student = Student(request.form['name'], request.form['stu_course'])
    db.session.delete(new_student)
    db.session.commit()
    jsonify("students.html")
    return jsonify(new_student.__repr__())


if __name__ == '__main__':
    app.run()
