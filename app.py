from cs50 import SQL
from flask import Flask, redirect, request, session, url_for, render_template
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import requests
import random
import os
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from helpers import login_required

db = SQL("sqlite:///project.db")
db.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL, username TEXT NOT NULL)"
)

db.execute(
    "CREATE TABLE IF NOT EXISTS playlists (user_id INTEGER NOT NULL, playlist_link TEXT NOT NULL, playlist_image TEXT, playlist_name TEXT NOT NULL, author TEXT NOT NULL)"
)

IMAGE_FOLDER = 'static/assets/login-page'
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

image_files = os.listdir(IMAGE_FOLDER)

# Spotify credentials
CLIENT_ID = 'client-id'
CLIENT_SECRET = 'client-secret'
REDIRECT_URI = 'http://localhost:5000/callback'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

# Spotify endpoints
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'


@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("email"):
            error = "Must provide email/username."
            return render_template("login.html", error=error)

        elif not request.form.get("password"):
            error = "Must provide password."
            return render_template("login.html", error=error)

        rows = db.execute(
            "SELECT * FROM users WHERE email = ? OR username = ?", request.form.get(
                "email"), request.form.get("email")
        )


        if len(rows) != 1  or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            error = "Incorrect username/password."
            return render_template("login.html", error=error)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    session.clear()

    if request.method == "POST":
        if not request.form.get("email"):
            error="Must provide email"
            return render_template('register.html', error=error)

        elif not request.form.get("password"):
            error="Must provide password"
            return render_template('register.html', error=error)

        elif not request.form.get("username"):
            error = "Must provide username"
            return render_template('register.html', error=error)

        elif request.form.get("password") != request.form.get("confirmation"):
            error="Password must be same as confirm password"
            return render_template('register.html', error=error)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        if len(rows) != 0:
            error = "Username already exists."
            return render_template('register.html', error=error)

        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get(
                "email")
        )

        if len(rows) != 0:
            error="Account with the given email already exists"
            return render_template('register.html', error=error)

        db.execute(
            "INSERT INTO users (email, hash, username) VALUES (?, ?, ?)",
            request.form.get("email"),
            generate_password_hash(request.form.get("password")),
            request.form.get("username")
        )

        return redirect("/")

    else:
        return render_template('register.html')



@app.route('/')
@login_required
def index():
    error = request.args.get('error', default=None)

    rows = db.execute(
        "SELECT * FROM playlists WHERE user_id = ?", session["user_id"]
    )

    if (len(rows) != 0):
        return render_template('index.html', error=error, rows=rows)

    return render_template('index.html', error=error)


@app.route('/get_image')
def get_image():
    # Randomly select an image from the list
    image_url = f'/static/assets/login-page/{random.choice(image_files)}'
    return image_url


@app.route('/logout')
@login_required
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the home page or login page
    return redirect(url_for('login'))

@app.route('/playlistInsert', methods=["POST", "GET"])
@login_required
def playlistInsert():
    if not request.form.get("playlistID"):
        return redirect(url_for('index', error='Invalid Playlist ID'))

    try:
        playlist_id = request.form.get("playlistID")
        results = sp.playlist(playlist_id)

        rows = db.execute(
            "SELECT * FROM playlists WHERE playlist_link = ?", playlist_id
        )

        if len(rows) != 0:
            return redirect(url_for('index', error='Playlist already there'))

        flag = False
        if results["images"] is None:
            flag = True

        if flag == False:
            db.execute(
                "INSERT INTO playlists (user_id, playlist_link, playlist_image, playlist_name, author) VALUES (?, ?, ?, ?, ?)",
                session["user_id"], playlist_id, results["images"][0]["url"], results["name"], results["owner"]["display_name"]
            )
        else:
            db.execute(
                "INSERT INTO playlists (user_id, playlist_link, playlist_name, author) VALUES (?, ?, ?, ?)",
                session["user_id"], playlist_id, results["name"], results["owner"]["display_name"]
            )

        return redirect(url_for('index'))
    except spotipy.exceptions.SpotifyException:
        return redirect(url_for('index', error='Invalid Playlist ID'))


