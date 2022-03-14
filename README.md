# CS50 Final Project: FINANCEA$Y
#### Video Demo: https://youtu.be/aJw_vMSndYM
The project consists in a personal financial Web Application where the user can Register/Log In and input incomes and expenses in order to keep track of their finances. The easiest way for the user to keep track of their incomes and expenses, combining a user friendly interface and just the right amount of features.
The application works both on mobile and desktop version. 
 
Technologies used: Python, SQLite, Jinja, HTML, CSS, Flask, among others. 

## Templates

Seven HTML templates where created, combining HTML, CSS and Jinja: 

#### Layout
Represents the base of all other templates, being extended my them. 

#### Log In
Log in page, with username and password inputs. 

#### Register 
Register page, with user name, password and confirmation of the password inputs.

#### Index
Homepage, displays two input options: income and expense, each one having their own categories. 
In the center, the user can check their balance, which is automatically updated every time a new income or expense is registered. 

#### History
Table containing history of all inputs, indicating the operation's category, type, value and time. 

#### Summary (in process) 
Template that is meant to display two tables, one for incomes and other for expenses, calculating the amount spent/received per category. This functionality is still being developed, tho. 

#### Apology
Template that display error messages triggered by eventual input errors. 

When the user logs out from the system, the application redirects to the Log In page.  

## Python Files
There are two Python Files in the project, the main one called app.py, where the magic happens, and another one called helpers.py

#### helpers.py
Auxiliary file, containing functions that are used in the main python file. 


#### app.py
The main backend file, in wich the routes of the application are defined. 
Most routes accepts both GET and POST methods, triggering different outcomes each. 
Each route contains code that avoids eventual input errors, such as wrong password, username already taken, or internal bugs, such as empty inputs in the database.

Session is imported from flask session in order to keep track of which user is logged in. 

SQL is imported from CS50 in order to use SQLite Database

The library werkzeug.security was imported in order to guaratee secure hash password storage.

App configured to auto-reload templates and to not store responses in cache. 

##### @app.route("/", methods=["GET", "POST"]): 
Defines the index template, the homepage. 
Login is required to access this page. 
When the user submit a form via POST method, there are four error checkings and preventions:
 1. Make sure income is a valid float number
 2. Make sure expense is a valid float number
 3. Avoid category error if user is inputting only expense or only income
 4. Avoid storage of empty values

If submited via GET, the route returns the index template, dysplaying the balance value in the balance div. 

Flexbox is used in CSS in order to display three different boxes. 

#### @app.route("/login", methods=["GET", "POST"])
Defines the log in page.
Firts, clear the session in order to forget any user_id. 
Then, if the method is POST, there are two error checkings: 
 1. Make sure username was submited, can't be left blank. 
 2. Make sure password was submited. 


If accessed via GET, simply renders the index template. 

#### @app.route("/register", methods=["GET", "POST"])
Defines the register page. 
When the user submit a form via POST method, there are three error checkings and preventions:
 1. Make sure password and confirmation match. 
 2. Make sure username and password were submited.
 3. Make sure username is not already taken (which is done by querying the database for that username, if len > 0, it means the username is already in use)
If there are no errors, a password hash is generated, which will be stored in the database with the username.  
Session is used to keep track of which user is logged in. 

If accessed via GET, simply renders the register template. 

#### @app.route("/logout")
Logs out the user, clearing the session and redirect to index. 

#### @app.route("/history")
Login is required to access this page. 
Displays history of operations, in a table that shows the value, type, category and time of submission. 

## CSS
File responsible for the styling of the application. 

## Database
The application is supported by a database file, finalproject.db, which contains two tables, users and balance, that, combined, keep track of the user's inputs. 
