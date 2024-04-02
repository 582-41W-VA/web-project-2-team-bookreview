### This README file details the project's architecture, and how to install and run it locally.

Project backend is built using Django framework.  Project name is LTR and it has one app installed named "bookreviews".
Frontend will be rendered using HTML templates styled with CSS and some jquery.
Book data is provided by a third party API - Google books api, in this case.

To install this project locally:
1. Clone this repository
2. Create a virtual environment with this command: `python -m venv .venv` or use `python3 -m venv .venv` depending on your python installation.
3. Activate the virtual environment with command: `source .venv/bin/activate` (if you're on Mac) or `source .venv/scripts/activate` (if you're on Windows)
4. Install Django with command: `pip install django`
5. Install reuqests with command: `pip install requests`
6. Run the server with command: `python manage.py runserver`
7. Run this command generate migration files: `python manage.py makemigrations`
8. Run this command to apply migration files to database: `python manage.py migrate`
9. Create a superuser with : `python manage.py createsuperuser`


