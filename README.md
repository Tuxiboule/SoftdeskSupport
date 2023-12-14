# SoftDeskSupport
![](icon.png)

## About

- An API to manage IT projects with multiples users
- Adheres to the security standards of OWASP and to the RGPD

## Features

- User can create :
  - Project with name, desc, type...
  - Issues about a project with name desc, priority...
  - Comments about an issue with desc...

- Management of read and write access rights:
  - Only the author of a ressource can update/delete it.
  - Contributors on a project can read all ressources about it (issues and comments).

## Usage

Make sure you have installed the required libraries and set up the virtual environment by executing the following commands. 
A `requirements.txt` file is provided for this purpose and can be used as follows:

```
pip install pipenv
pipenv shell
pipenv install -r requirements.txt
```

Next, run the Python script `manage.py` to run the server at http://127.0.0.1:8000/

```
python manage.py runserver
```





## Context - Create a secure RESTful API using Django REST

- Second use of Django, this time to create an API.
- I liked a lot discovering Postman and creating a test environment inside.
- Adheres to OWASP and RGPD guidelines.
- Testing an API has been more challenging than testing a website because there is no front-end.

## Skills

- Django Rest Framework
- API creation
- SQLite Database
- Endpoint testing with Postman
- Greencode

## Credits
[Tuxiboule](https://github.com/Tuxiboule)
