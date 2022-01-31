from flask import Flask, request, jsonify, make_response   
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import jwt
import datetime
from functools import wraps


app = Flask(__name__) 


app.config['SECRET_KEY'] = 'este_es_un_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/michael/geekdemos/geekapp/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)   

class Users(db.Model):  
  email = db.Column(db.String(50), primary_key=True)
  password = db.Column(db.String(50))

def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
       token = None 

       if 'x-access-tokens' in request.headers:  
          token = request.headers['x-access-tokens'] 

       if not token:  
          return jsonify({'message': 'a valid token is missing'})   

       try:  
          data = jwt.decode(token, app.config[SECRET_KEY]) 
          current_user = Users.query.filter_by(public_id=data['public_id']).first()  
       except:  
          return jsonify({'message': 'token is invalid'})  

          return f(current_user, *args,  **kwargs)  
    return decorator 


@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
  data = request.get_json()  
  hashed_password = generate_password_hash(data['password'], method='sha256')

  new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False) 
  db.session.add(new_user)  
  db.session.commit()    

  return jsonify({'message': 'registered successfully'})   


@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  user = Users.query.filter_by(name=auth.username).first()   

  if check_password_hash(user.password, auth.password):  
    token = jwt.encode({'email': user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
    return jsonify({'token' : token.decode('UTF-8')}) 

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/user', methods=['GET'])
def get_all_users():  
   users = Users.query.all() 
   result = []   

   for user in users:   
       user_data = {}   
       user_data['email'] = user.email  
       user_data['password'] = user.password
       
       result.append(user_data)   

   return jsonify({'users': result})  


@app.route('/cases', methods=['GET', 'POST']) 
@token_required 
def get_cases(current_user, public_id):  
    cases = [1, 2, 3, 4]
    return jsonify({'cases' : cases})


@app.route('/cases/<name>', methods=['GET'])
@token_required
def delete_author(current_user, name):
    return jsonify({'message': 'Case ' + name})


if __name__ == '__main__':
    app.run(debug=True)
