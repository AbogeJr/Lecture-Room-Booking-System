from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref, joinedload
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

#Init class_rep
class classRep(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    regNo = db.Column(db.String(80), unique=True)
    unitCode = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80), unique=True)

    def __int__(self, name, regNo, unitCode, password):
        self.regNo = regNo
        self.name = name
        self.unitCode = unitCode
        self.password = password

# class_repSchema
class class_repSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name',  'regNo', 'unitCode')

# Init class_repSchema 
class_rep_schema = class_repSchema() 
class_reps_schema = class_repSchema(many=True)

#room class/Model
class lectureRoom(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(80), unique=False)
    room = db.Column(db.String(80), unique=False)
    unit = db.relationship('unit', backref = 'lecture_room')

    def __int__(self, school, room, unit):
        self.room = room
        self.school = school
        self.unit = unit

#  roomSchema
class roomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'school', 'room', 'unit')

#Init roomSchema
room_schema = roomSchema()
rooms_schema = roomSchema(many=True)


# Init units
class Unit(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    unitTitle = db.Column(db.String(80), unique=False)
    unitCode = db.Column(db.String(40))
    school = db.Column(db.String(80), db.ForeignKey(lectureRoom.school))

    def __int__(self, school, unitTitle, unitCode):
        self.unitTitle = unitTitle
        self.school = school
        self.unitCode = unitCode

# unitSchema
class unitSchema(ma.Schema):
    class Meta:
        fields = ('id', 'school', 'unitTitle', 'unitCode')

#Init unitSchema
unit_schema = unitSchema()
units_schema = unitSchema(many=True)

#Init query
#query = lectureRoom.query.options(joinedload('units'))
#for lectureroom in query:
    #print (school, unit)

# add a room
@app.route('/lecture-rooms', methods =['POST'])
def add_lecture_rooms():
    school = request.json['school']
    room = request.json['room']

    new_room = lectureRoom(school, room)
    db.session.add(new_room)
    db.session.commit()

    return room_schema.jsonify(new_room)

# add a unit 
@app.route('/unit', methods =['POST'])
def add_unit():
    unitTitle = request.json['unitTitle']
    unitCode = request.json['unitCode']
    school = request.json['school']

    new_unit = Unit(unitTitle, unitCode, school)
    db.session.add(new_unit)
    db.session.commit()

    return unit_schema.jsonify(new_unit)

# add a class_rep 
@app.route('/class-rep', methods =['POST'])
def add_class_rep():
    regNo = request.json['regNo']
    name = request.json['name']
    unit = request.json['unit']
    password = request.json['password']

    new_class_rep = classRep(regNo, name, unit, password)
    db.session.add(new_class_rep)
    db.session.commit()

    return class_rep_schema.jsonify(new_class_rep)





if __name__ == '__main__':
    app.run(debug=True)
