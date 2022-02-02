from flask import Flask, request, jsonify, make_response   
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_marshmallow import Marshmallow
from enum import Enum


app = Flask(__name__) 

app.config['SECRET_KEY'] = 'este_es_un_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

with app.app_context():
  db.create_all()

# ------
# Enums
# ------
class Categories(str, Enum):
  CONFERENCE = "Conferencia"
  SEMINAR = "Seminario"
  CONGRESS = "Congreso"
  COURSE = "Curso"

class Modalities(str, Enum):
  FACE_TO_FACE = "Presencial"
  VIRTUAL = "Virtual"

# ---------------------
#  Classes and schemas
# ---------------------
class User(db.Model):
  __tablename__ = "user"
  email = db.Column(db.String(50), primary_key=True)
  password = db.Column(db.String(50))
  events = db.relationship("Event", backref="event", cascade="all, delete-orphan")

class User_Schema(ma.Schema):
  class Meta:
    fields = ("email", "password")

class Event(db.Model):
  __tablename__ = "event"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  category = db.Column(db.String(50))
  place = db.Column(db.String(255))
  address = db.Column(db.String(255))
  start = db.Column(db.DateTime)
  end = db.Column(db.DateTime)
  modality = db.Column(db.String(50))
  owner = db.Column(db.String(50), db.ForeignKey("user.email"), nullable=False)

class Event_Schema(ma.Schema):
  class Meta:
    fields = ("id", "name", "category", "place", "address", "start", "end", "modality", "owner")

user_schema = User_Schema()
users_schema = User_Schema(many=True)

event_schema = Event_Schema()
events_schema = Event_Schema(many=True)

# ---------------
# Auth function
# ---------------
def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None
    if 'Authorization' in request.headers and 'Bearer' in request.headers['Authorization']:
      token = request.headers['Authorization'].split(" ")[1]
      print("Token", token)
    if not token:
      return jsonify({'message': 'unauthorized'})
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
      current_user = User.query.filter_by(email=data['email']).first()
    except:
      return jsonify({'message': 'token is invalid'})
    return f(*args, current_user, **kwargs)
  return decorator

# --------------
# API Resources
# --------------
class SignupResource(Resource):
  def post(self):
    data = request.json
    print(data)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=data['email'], password=hashed_password) 
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})

class LoginResource(Resource):
  def post(self):
    # auth = request.authorization
    # if not auth or not auth.email or not auth.password:
    # return make_response('unauthorized', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    
    user = User.query.filter_by(email=request.json['email']).first()

    if user and check_password_hash(user.password, request.json['password']):
      token = jwt.encode({'email': user.email, 'exp' : datetime.utcnow() + timedelta(hours=2)}, app.config['SECRET_KEY'])  
      return jsonify({'token' : token})
    else:
      return make_response('Wrong user or password', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

class EventsResource(Resource):
  @token_required
  def get(self, current_user):
    print("No sé qué poner", self)
    print("No sé qué poner", current_user)
    events = Event.query.filter_by(owner=current_user.email).all()
    return events_schema.dump(events)
  
  @token_required
  def post(self, current_user):
    new_event = Event(
      name = request.json['name'],
      category = request.json['category'],
      place = request.json['place'],
      address = request.json['address'],
      start = datetime.strptime(request.json["start"], "%d/%m/%Y"),
      end = datetime.strptime(request.json["end"], "%d/%m/%Y"),
      modality = request.json['modality'],
      owner = current_user.email
    )
    print(new_event)
    db.session.add(new_event)
    db.session.commit()
    return event_schema.dump(new_event)

class SpecificEventResource(Resource):
  @token_required
  def get(self, event_id):
      event = Event.query.get_or_404(event_id)
      return events_schema.dump(event)
  
  @token_required
  def put(self, current_user, event_id):
      event = Event.query.get_or_404(event_id, owner=current_user.email).first()
      if 'title' in request.json:
          event.title = request.json['title']
      if 'content' in request.json:
          event.content = request.json['content']

      db.session.commit()
      return events_schema.dump(event)

  @token_required
  def delete(self, event_id):
      publicacion = Event.query.get_or_404(event_id)
      db.session.delete(publicacion)
      db.session.commit()
      return '', 204

api.add_resource(SignupResource, '/auth/signup')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(EventsResource, '/events')
api.add_resource(SpecificEventResource, '/events/<int:event_id>')

if __name__ == '__main__':
    app.run(debug=True)
