# CRM_Epic_Event
Creation of CRM for the P12

This API will serve for multi-platform applications. Applications will allow users to manage their clients.

**FEATURES**
* Create users with the admin interface of the API
* login users
* CRUD on clients
* CRUD on events
* CRUD on contracts

## A- Cloned the GitHub project 
### 1- Create a folder and place yourself inside it.
    whith linux :
    $ mkdir CRM_Epic
    $ cd CRM_Epic
### 2- Clone the GitHub folder "softdeskAPI"
    $ git clone https://github.com/AnaisG14/CRM_Epic_Event.git
### 2- Create and active a virtual environment (with linux):
#### -> Create the virtual environment
    Place yourself in the cloned folder
    $ cd CRM_EpicEvent
    $ python3 -m venv <environnement name>

    exemple: 
    $ python3 -m venv envCRM
#### -> Active your virtual environment
    $ source <environnement_name>/bin/activate

    exemple : 
    $ source envCRM/bin/activate
### 3- Install the required packets :
    $ pip install -r requirements.txt

## B- Manage the db with PostGreSql
### 1- Install  et configurer PostGre dans les settings
    https://doc.ubuntu-fr.org/postgresql

### 2- Create a super User
    $ python manage.py createsuperuser
    And enter a name and a password (the email address is optional)
### 3- Manage the db on a browser
    http://127.0.0.1:8000/admin/

## C- Documentation