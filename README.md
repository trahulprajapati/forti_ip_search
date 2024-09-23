### Project overview
Refer ./documents
<br>
<br>

### Solution Architecture
Refer ./documents
<br>
<br>

### HLD Documents
Refer ./documents
<br>
<br>

### Project Directory structure
#### api/
This contains all controllers, services and serielisers, Dependecy injection, 
API Rest resource contain in controllers
#### celery_app
worker are celery app contain im this folder
#### common
Constant ans utils classes.
#### config
Config files for prod, dev, uwsgi.ini and common in both
#### docker
Docker file for flask app and celery
#### documents
HLD document
#### mixins
Common mixins that can be used indifferent app.
#### static
This contains json source file which all all the details for subnet.
#### tests
Testcase coverage for API endpoints
#### .env
Envirornment variables, used in app startuo in dkcer env
#### docker-compose
Contain all services, which all services should be running when app is running.
#### requirements.txt
All dependency for prod env
#### requirements-dev.txt
All dependency for dev env
#### requirements-celert.txt
All dependency for celery worker
#### server.txt
Flask app
#### setup
Packaging application.
#### wsgi.py
Used to run aplication, used by config/uwsgi.ini
uwsgi server will use this it start the flask app.
#### .dockerignore and .gitignore
File to exclude from git and docker.


<br>
<br>

### Setup dev envirorment

### Setup docker env
Clone repo and follow below steps
```commandline
git clone https://github.com/trahulprajapati/forti_ip_search.git
cd <project_home>
```
#### Setup docker-compose env
```commandline
docker-compose build
docker-compose up -d

```
Check the status container is up and running
```commandline
docker-compose ps -a
```


### Setup docker env
```commandline
docker build --tag dkr:latest .
docker run --name dkr -d -p 8000:8000 dkr:latest
```
You can access application via:
```commandline
http://127.0.0.1:8000/
```

<br>
<br>

### Setup dev env normal (without docker)
Install python3.8.13
Install virtual env package
```commandline
pip install virtualenv
```
Create virtual out of your project home(adjacent to project root directory)
```commandline
python3.11 -m virtualenv ip_search
source ./ip_service_env/bin/activate
```
Change directory project home and install requirement.txt file
```commandline
pip install -r requirement.txt
```

#### Run server
uwsgi --ini config/uwsgi.ini

```
