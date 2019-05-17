import os

import hashlib
import sys
import requests
import json
import pylint_flask
from flask import Flask, session, render_template, request
from flask_session.__init__ import Session
import flask_sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, session, sessionmaker

app = Flask(__name__)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    booksIndex = db.execute("SELECT * FROM books").fetchall()
	headline = "Project 1: Welcome to Book Review!"
    return render_template ("index.html", headline=headline)

@app.route("/register", methods=["GET", "POST"])
def register():
	headline = "Register Here!"
	return render_template ("register.html", headline=headline)

@app.route("/save_registration", methods=["GET", "POST"])
def save_registration():
	if request.method == "GET":
		return "Operation not permitted.  Stop trying to hack the system."
	else:
		usernameReg = request.form.get("username")
		passwordReg = request.form.get("password")
		users = db.execute("INSERT INTO users (userid, username, password) values (nextval('userIDSeq'), :username, :password)",{"username": usernameReg, "password": passwordReg})
		return render_template("success.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	headline="Welcome back!  You can login here."

	#get username and password
	username = request.form.get("username")
	password = request.form.get("password")

	#check it
	user = db.execute("SELECT * FROM users WHERE username =:username", {"username":username}).fetchall()
	#if they didn't fill out all fields
	if not user or not username or not password:
		return render_template('login.html', message="Missing username or password.", logIn=False)
	#if they completed the form correctly
	else:
		#if the username/password combo works
		if password == user[0][3]:
			return render_template("login.html", message="You have successfully logged in.")
		#if it doesn't
		else:
			return render_template("login.html", message="Incorrect username/password combination.")
@app.route("/logout")
def logout():
	session.pop('userid', None)
	return index()

@app.route("/search")
def search():
	return render_template ("search.html")

@app.route("/books", methods=["GET", "POST"])
def books():
	#if there's nothing in books, make an empty dict
	if session.get("books") is None:
		session["books"] = []
	if request.method == "POST":
		book = request.form.get("book")
		session["books"].append(book)
	return render_template("books.html", books=session["books"])

