# Conservify
#### Video Demo:  <URL HERE>
#### Description:
This project is a dynamic web application built using Flask and JavaScript. It allows users to register and log in, manage their Spotify playlists, and view detailed information about each playlist. The application features dynamic background changes, secure user authentication, and interaction with Spotify's Web API to retrieve playlist details.

app.py
This file contains most of the flask functionalities, connects to spotify making sure that the playlist link uploaded is proper and not already in the database, manage the user accounts like hashing the passwords, storing them in the database, making sure that the passwords match with the username/email given, check if the username/email provided in register already exists or not. It is also helpful in error handling in the given scenarios, giving proper and brief error messages when required. Also makes sure to clear the session when user logs out. The functionality of inserting a playlist's link, name, cover image and author is also done by this app. It also makes sure that the routes which require login can't be accessed without doing so.

helpers.py
It doesn't have much but is required for defining the wrapper for login required. This wrapper is essential in making sure that pages like index, or playlistInsert can't be accessed without loggin in first.

project.db
This file is the database file, mainly responsilbe for storing user's data, such as their password's hash, their account email address, and username. This database has another table responsible for storing a playlist's link, name, cover image and author while also linking that playlist with the respective user, making sure that one can only access their own playlists.

templates/layout.html
Mainly responsible for providing the boilerplate code and remove redunancy in the code. This ensures that the bootstrap library and our own stylesheet is linked with the pages, so that the styles can be carried throughout the pages.

templates/login.html
This page is responsible for the logging in of the user. It contains a background image which changes after every 30 seconds. The page also has a form which has two text fields, one for username/email and one for password. Linking it with app.py, it checks whether the information provided is correct or not and gives an error message if not done so. There is also a redirect link to the register page for easy access of users who are new to the site and have not registered yet.

templates/register.html
Similarly, this site is responsible for registration of new accounts to the database. Connecting this with app.py allows us to make sure that an already registered email is not being registered through again. There are multiple fields present in the form such as email, username, password and confirm-password. If any of these fields are left blank then it makes sure to inform that to the user and doesn't proceed the registration procedure forward until every field is fulfilled. This site also has a background which changes every 30 seconds. There is also a redirect to the login page for those who realize that they have already registered or want to visit the login page for any other reason.

templates/index.html
This page is the main home page of the entire website. It has a nav bar at the top containing only one option, which is logout. When pressed, the session is cleared and user logs out of the website and will have to log back in for visiting the homepage again. There is a form present in the page where the user can paste their spotify playlist's link. Using app.py, the playlists are verified through Spotify's web API. If the playlist link doesn't work or is private, the user is informed so through the error message. It also makes sure that already added playlists can't be added again, and if tried by any user, they are informed that the playlist already exists by the website. When a valid playlist link is submitted through the form, then using app.py, the playlist's name, author and cover image is stored inside the database.
In the right side the playlists are visible inside a table. These playlists are shown through some jinja code and linking with app.py. In addition to that using Javascript, when any of the rows in this table are pressed, the playlist table goes to a hidden state, while another tracks-table goes to visible state. This table then uses the link of the playlist present in that row. Using Spotify's API, we access the tracks present in that playlist and then empty the tabe and then insert all of the tracks of the current playlist into the table. There is a back button at the top of this table, which when pressed changes the visibility of this table to hidden and that of the playlist-table to visible. There is also a download button at the top of the tracks table. This is useful for downloading the entire playlist in the form of a .csv file. As visible, the table only shows atmost 4 tracks at a time, but there are buttons at the bottom named up and down for the scrolling purposes. These are achieved through maintianing an index variable.

static/styles.css
This is only used for storing the routes to fonts so that they can be easily referenced in the html files.

static/assets/fonts
This folder contains the fonts downloaded externally to be used in this project.

static/assets/login-page
This folder contains the background images which are changing by in the login page and register page.

# Features
## User Registration and Login:

Users can register and log in to the application.
Passwords are hashed using the werkzeug.security library for secure storage.
User details are stored in a local SQLite database for future logins.

## Dynamic Backgrounds:

The login and register pages feature backgrounds that change every 30 seconds using JavaScript.
Background images are sourced from Behance. https://www.behance.net/gallery/189990959/Moving-to-the-Beat-Spotify

## Font Integration:

The fonts used in the application are:
Heroeau Elegant: Used on the login and register pages, sourced from 1001Fonts.
Porcine Font: Used for playlist names, sourced from FreeDaFonts.

## User Dashboard:

Upon logging in, users are redirected to a dashboard.
The dashboard features a navbar with a logout option and a form for submitting Spotify playlist links.

## Playlist Management:

Users can submit Spotify playlist links to add playlists.
If an incorrect playlist link is provided or the playlist is already in the user's database, an error message is displayed.
Playlist details (link, image, name, author) are fetched using Spotify's Web API and stored in the database linked to the user's ID.

## Playlist Display:

Playlists are displayed in a table on the right side of the dashboard using Jinja syntax.
Hovering over a playlist row shows a slight green shadow.
Clicking a playlist row hides the current table and shows a detailed table of tracks in the playlist.

## Track Details and Interaction:

The detailed table shows track names, artists, and album images using Spotify's Web API.
A back button allows users to return to the playlist table.
Tracks are displayed four at a time, with up and down buttons for scrolling.

## CSV Download Functionality:

Users can download track details as a CSV file.
This is achieved using simple JavaScript for file generation and download.
