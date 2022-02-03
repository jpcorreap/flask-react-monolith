from flask import Flask, request, jsonify, make_response   
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import except_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, JWTManager
from datetime import datetime, timedelta
from functools import wraps
from flask_marshmallow import Marshmallow
from enum import Enum
from flask_cors import CORS


app = Flask(__name__, static_folder="front/build", static_url_path="/")
CORS(app)

app.config['SECRET_KEY'] = 'este_es_un_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

with app.app_context():
  db.create_all()

jwt = JWTManager(app)

# ------------------
# Acts kind of enums
# ------------------
valid_categories = ["Conferencia", "Seminario", "Congreso", "Curso"]
valid_modalities = ["Presencial", "Virtual"]

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
    user = User.query.filter_by(email=request.json["email"]).first()
    if check_password_hash(user.password, request.json["password"]):
      access_token = create_access_token(
        identity=user.email, expires_delta=timedelta(hours=2)
      )
      return {"token": access_token}, 200
    else:
      return "Wrong email or password", 401

class EventsResource(Resource):
  @jwt_required()
  def get(self):
    events = Event.query.filter_by(owner=get_jwt_identity()).all()
    return events_schema.dump(events)
  
  @jwt_required()
  def post(self):
    if request.json['category'] not in valid_categories:
      return make_response('Invalid category, it must be at least one of: ' + ', '.join(valid_categories), 400)
    if request.json['modality'] not in valid_modalities:
      return make_response('Invalid modality, it must be at least one of: ' + ', '.join(valid_modalities), 400)
    new_event = Event(
      name = request.json['name'],
      category = request.json['category'],
      place = request.json['place'],
      address = request.json['address'],
      start = datetime.strptime(request.json["start"], "%d/%m/%Y"),
      end = datetime.strptime(request.json["end"], "%d/%m/%Y"),
      modality = request.json['modality'],
      owner = get_jwt_identity()
    )
    try:
      db.session.add(new_event)
      db.session.commit()
      return event_schema.dump(new_event)
    except:
      return make_response('Error', 400)

class SpecificEventResource(Resource):
  @jwt_required()
  def get(self, event_id):
    event = Event.query.filter_by(owner=get_jwt_identity(), id=event_id).first_or_404()
    return event_schema.dump(event)
  
  @jwt_required()
  def put(self, event_id):
    event = Event.query.get_or_404(id=event_id, owner=get_jwt_identity()).first()
    if request.json['category'] not in valid_categories:
      return make_response('Invalid category, it must be at least one of: ' + ', '.join(valid_categories), 400)
    if request.json['modality'] not in valid_modalities:
      return make_response('Invalid modality, it must be at least one of: ' + ', '.join(valid_modalities), 400)
    event.name = request.json["name"]
    event.category = request.json["category"]
    event.place = request.json["place"]
    event.address = request.json["address"]
    event.start = datetime.strptime(request.json["start"], "%Y-%m-%d")
    event.end = datetime.strptime(request.json["end"], "%Y-%m-%d")
    event.modality = request.json["modality"]
    db.session.commit()
    return event_schema.dump(event)

  @jwt_required()
  def delete(self, event_id):
    events = Event.query.filter_by(owner=get_jwt_identity(), id=event_id).first_or_404()
    db.session.delete(events)
    db.session.commit()
    return 'Deleted', 200

api.add_resource(SignupResource, '/auth/signup')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(EventsResource, '/events')
api.add_resource(SpecificEventResource, '/events/<int:event_id>')

@app.route("/")
def serve():
    return app.send_static_file("index.html")

if __name__ == '__main__':
    app.run(debug=True)
