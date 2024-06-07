from flask import Flask
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions.database import db
from extensions.auth import jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SECRET_KEY'] = "test"

db.init_app(app)
jwt.init_app(app)
CORS(app)

@app.route("/login", methods=["POST"])
def login():
  data = request.json
  email = data.get("email")
  password = data.get("password")
  # do validation
  if not email or not password:
    return jsonify({"error": "Missing data"}), 400
  # get user
  user = db.session.query(User).filter(User.email == email).first()
  if not user:
    return jsonify({"error": "Invalid credentials"}), 400
  # check password
  if not check_password_hash(user.password, password):
    return jsonify({"error": "Invalid credentials"}), 400
  access_token = create_access_token(identity=user.id)
  return jsonify({"message": "Logged in", "access_token": access_token})



@app.route("/signup", methods=["POST"])
def signup():
  data = request.json
  first_name = data.get("first_name")
  last_name = data.get("last_name")
  email = data.get("email")
  password = data.get("password")
  # do validation
  if not first_name or not last_name or not email or not password:
    return jsonify({"error": "Missing data"}), 400
  # check if email is unique
  if db.session.query(User).filter(User.email == email).first():
    return jsonify({"error": "Email already exists"}), 400
  # hash password
  hashed_password = generate_password_hash(password)
  # create user
  user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
  db.session.add(user)
  db.session.commit()
  return jsonify({"message": "User created"}), 201




@app.route("/me")
@jwt_required()
def me():
  identity = get_jwt_identity()
  user = db.session.query(User).get(identity)
  if not user:
    return jsonify({"error": "User not found"}), 404
  return jsonify({"first_name": user.first_name, "last_name": user.last_name, "email": user.email})


