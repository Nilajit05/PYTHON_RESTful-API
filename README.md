# PYTHON_RESTful-API
Create a RESTful API with:
1. A linked database (use SQLite or some other file database if no database servers are
available) with a user table containing the below fields:

a. id
b. first_name
c. last_name
d. age
e. gender
f. email
g. phone
h. Birth_date

2. Endpoint /api/users with a mandatory query parameter: first_name.
3. Feature for searching the user table for all users with the beginning of first_name
matching the param first_name.
For example: "will" will match both "will" and "william".
a. If users are found then return the list of matching users in a JSON response.
b. Else call the API: https://dummyjson.com/users/search?q=first_name
with the first_name parameter, save the resulting users to the user table and return
them in the response.

Let's go through the entire process of creating and completing the RESTful API project step by step:
Step 1: Set Up Your Development Environment
Install Python and Flask:

Install Python on your computer.
Open a terminal (command prompt) and install Flask using the command: 'pip install Flask'.
Create a Project Directory:

Create a new directory for my project, for example: RESTfulAPI.
Navigate to Your Project Directory:

Open the terminal and navigate to your project directory.
Step 2: Create the Database and Tables
Create a SQLite Database:

Open a terminal and navigate to the project directory.
Run the SQLite command to create a new database: 'sqlite3 db/database.db'.
Create the User Table.
Step 3: Set Up the Flask Application
Create the Flask App:

In the project directory, create a new Python file named app.py.
Import Necessary Modules:

Import Flask and other required modules at the top of app.py.
Configure the Database Connection:

Define functions to create a database connection and insert user data.
Create the Hello World Endpoint:
Define a simple route in the Flask app that returns "Hello, World!" when accessed.

Step 4: Implement the /api/users Endpoint
Create the /api/users Endpoint:
Define a route for the '/api/users' endpoint that handles both GET and POST requests.
Implement the 'get_users()' function to retrieve users from the database and return a JSON response.
Implement the 'add_user()' function to add a new user to the database and return a success message.

Step 5: Implement User Search and DummyJSON Integration
Implement User Search:

Add a route parameter 'first_name' to the '/api/users' endpoint.
Modify the 'get_users()' function to handle user search based on the 'first_name' parameter.
Step 6: Run and Test the Application
Run the Flask App:

In the terminal, run your Flask app using the command:' python app.py'.
Access Endpoints:

Open your web browser or use tools like Postman to access the various endpoints:
'http://127.0.0.1:5000/': Hello World endpoint
'http://127.0.0.1:5000/api/users': List users
'http://127.0.0.1:5000/api/users?first_name=will': Search users by first name
