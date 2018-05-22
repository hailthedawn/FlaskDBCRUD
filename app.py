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


db.create_all()
#db.drop_all()


@app.route('/', methods=['GET'])
def home():
    # TODO use JSON
    examples = Student.query.all()
    db.session.commit()
    return render_template("students.html", rows=examples)


@app.route('/add-student', methods=['POST'])
def post_student():

    student_dict = request.get_json('name')

    new_student = Student(name=student_dict.get('name'), stu_course=student_dict.get('stu_course'))
    # new_student = Student(request.form['name'], request.form['stu_course'])   #TODO without passing primary key
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.__repr__())


@app.route('/update-student', methods=['POST'])
def update_student():

    new_student = Student.query.filter_by(name=request.get_json('name').get('name')).first()
    new_student.stu_course = request.get_json('stu_course').get('stu_course')
    db.session.commit()
    return jsonify(new_student.__repr__())


@app.route('/remove-student', methods=['POST'])
def remove_student():
    # student_dict = request.get_json('name')

    new_student = Student.query.filter_by(name=request.get_json('name').get('name')).first()
    db.session.delete(new_student)
    db.session.commit()
    return jsonify(new_student.__repr__())


if __name__ == '__main__':
    app.run()
