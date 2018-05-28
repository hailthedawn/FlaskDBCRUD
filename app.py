from flask import render_template, redirect, request, url_for
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
#import PasswordEncrypt

#from PasswordEncrypt import GlobalUser

app=Flask(__name__)

#globalUser = GlobalUser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskuser:flask@12345@localhost/students'
#app.config(SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" + globalUser.username + ":" + globalUser.password + "@127.0.0.1:54990/students")
db = SQLAlchemy(app)                                #
db.session.commit()


class Student(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(64), unique=True)
    stu_course = db.Column('stu_course', db.String(64))

    def __init__(self, name, stu_course):
       # self.id=id
        self.name = name
        self.stu_course = stu_course

    def serialize(self):
        """
        Helper function to serialize a student
        :return:
        """
        return {'id': self.id, 'name': self.name, 'course': self.stu_course}

    def __repr__(self):
        return 'id={}, name={}, course={}'.format(self.id, self.name, self.stu_course)



db.create_all()
#db.drop_all()


@app.route('/')
def home():
    """
    A simple home page.
    :return: A welcome message
    """
    return "Welcome to this CRUD App."


@app.route('/students', methods=['GET'])
def show_students():
    """
    Displays all students in the database.
    :return: all students in html format
    """
    # TODO use JSON
    all_students = {}
    try:
        entries=Student.query.all()

        if(len(entries) == 0):
            return jsonify("No students in database.")

        db.session.commit()
        return jsonify([entry.serialize() for entry in entries])

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)




@app.route('/student', methods=['POST'])
def post_student():
    try:

        student_dict = request.get_json('name')
        check_validity(student_dict)

        new_student = Student(name=student_dict.get('name'), stu_course=student_dict.get('stu_course'))
        # new_student = Student(request.form['name'], request.form['stu_course'])   #TODO without passing primary key
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.serialize())

    except Exception:
        return "Specified username already in database."


@app.route('/student/<stu_id>', methods=['PUT'])
def update_student(stu_id):
        try:
            new_student = Student.query.filter_by(id=stu_id).first()
            new_student.name = request.get_json('name').get('name')
            new_student.stu_course = request.get_json('name').get('stu_course')

            db.session.commit()
            return jsonify(updated= 'Success', student= new_student.serialize())

        except Exception:
            return "No such user in database, or new user already exists."


@app.route('/student/<stu_id>')
def display_student(stu_id):
    new_student = Student.query.filter_by(id=stu_id).first()
    if new_student == None:
        return "No such user exists."
    return jsonify(new_student.serialize())


@app.route('/student/<stu_id>', methods=['DELETE'])
def remove_student(stu_id):
    # student_dict = request.get_json('name')
    # print("here")
    try:
        new_student = Student.query.filter_by(id=stu_id).first()
        db.session.delete(new_student)
        db.session.commit()
        return jsonify(removed= 'Success', student=new_student.serialize())
    except Exception:
        return "Cannot remove a student that doesn't exist in database."


def check_validity(input_dict):
    """
    Checks for validity of input.
    :param:     the input request in dict format
    :return:    error status and details in dict formmat
    """
    error_dict={}
    error = False
    if input_dict.get('name')==None:
         error=True
         error_dict['name'] = 'was null'
    if input_dict.get('stu_course')==None:
        error=True
        error_dict['course'] = 'was null'
    error_dict['error'] = error
    return error_dict


if __name__ == '__main__':
    app.run()