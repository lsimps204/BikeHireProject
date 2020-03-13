# BikeProject

## Technical Overview

The application uses the Django framework and Python 3.* for the backend implementation of the project. Additional Python tools such as *NumPy*, *Matplotlib*, *Bokeh*, *GeoPy* and *Networkx* are used to deliver some of the analysis and visualization features of the project. 

The database used is **Sqlite**, but this can be easily switched out for MySQL or PostgreSQL. The migration-related commands outlined in the **setup** section below will take care of creating this database from scratch.

Note: use an alternative database, you must edit the project's `settings.py` file and provide database connection information. Additional packages will also need to be installed, for example the *psycopg2* package for enabling operations on the PostgreSQL database.

The front end of the application is delivered using standard front-end web technologies, such as HTML for structuring content, CSS for design (and the Bootstrap framework), and JavaScript/jQuery for implementation of interactive functionality and AJAX requests.

## Setup

To set up the project, first navigate via the terminal to the directory where the project code resides. The root directory, containing the `manage.py` file, should be the current working directory in the terminal in order for the commands below to work.

Once in the correct location, the following commands should be run (in this order):

1. `python -m pip install -r requirements.txt` - this command will install the project requirements (external Python libraries).

2. `python manage.py makemigrations` - this command will generate Database migrations

3. `python manage.py migrate` - this command will create the SQLite database from the migrations created above

4. `python manage.py add_bike_data` - this command will generate a set of bikes, locations and users for the application, as well as "fake" historical data for the application.

5. `python manage.py runserver` - this command will run the development server, allowing the user to test the application at the link: `localhost:8000


## Sample Users

In the application, users are grouped into 3 user types:

1. Customers - standard users who can hire bikes, view their hire history, view location data, and view their own profiles.
2. Operators - in addition to the above, can also view an "Operators" page with more specific, priviledged operations
3. Managers  - in addition to the above, can also view a "Reports" page with application-specific reports

The following 'fake' users were created in the script run in **Step 4** of the setup, for convenience when testing. Note: you can also create new users from the login/register pages, but these will always be set to "Standard" users.

1. Manager user: `lyle`, password: `password`
2. Operator user: `operator1`, password `password`
3. Customer user : `customer1`, password: `password`
