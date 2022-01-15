# Audiobooks backend

This project is created to allow users quickly find audioboooks that are translated to Belarusian 

## Project structure
* booksby - main project folder with settings and project top url setup
* books, user, person - apps for each instance 
* templates - all html templates based on each other
* static - static files, css, js, images
* data - contains data.json with books data and scripts that synchronize data. See Books Data section below.

## Backend setup

**Note: You should have Python and Postgresql installed on your local env**

### Update ENV

Rename .env.dist to .env
Update values:
* DEBUG=True for dev env
* SECRET_KEY=_any symbols for dev, don't change in prod_
* ALLOWED_HOSTS=localhost for local
* DATABASE - your Postgres DB values to connect to local DB

### Create Python virtual enviroment

Ensure venv is installed:
```
apt-get install python3-venv
```

In the project folder run:
```
python -m venv ./venv
source ./venv/bin/activate
```

### Install all dependencies

When virtual enviroment is activated in the step above:
**Note: comment psycopg2 in requirements.txt if you're using Mac with M1 chip**
```
pip install -r requirements.txt
```

### Test initial state
**Note: Depends on your python installation you might need to user `python3` instead of `python` in the commands below**
```
python manage.py runserver
```
check in the browser that you can see home page: http://127.0.0.1:8000/

### Setup django and project:

Run in the project folder:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Create superuser creds to access Admin site at: http://127.0.0.1:8000/admin

### Run the project:
```
python manage.py runserver
```

## Books data

Data about books, authors, narrators, translators and so on is currently stored in `data.json` file in `data` folder. There are scripts in that folder that can update the JSON file synchronizing its data with external resources such as https://knizhnyvoz.by, podcasts, https://litres.ru and others. Each script is called syncer and starts with `sync_` prefix. To update data do the following:

1. Run a syncer script from project rood directory: `python -m data.sync_knizhny_voz`. 
2. Check changes in data.json: `git diff data/data.json` or using any other diff tool.
3. If found an issue - update the script or fix the data manually. Though better update the script to automate issue in future. It's ok to have hardcoded one-off fixes.
4. When done - commit `data.json` changes.


