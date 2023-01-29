# Sersky the flasky 'like' headless server

# Status codes:

200 OK The request was completed successfully.

201 Created The request was completed successfully and a new resource was created as a result.

202 Accepted The request was accepted for processing, but it is still in progress and will run
asynchronously.

204 No Content The request was completed successfully and there is no data to return in the response.

400 Bad Request The request is invalid or inconsistent.

401 Unauthorized The request does not include authentication information or the credentials provided are
invalid.

403 Forbidden The authentication credentials sent with the request are insufficient for the request.

404 Not Found The resource referenced in the URL was not found.

405 Method Not Allowed The method requested is not supported for the given resource.

500 Internal Server Error An unexpected error occurred while processing the request.

## Build

- set venv
- sqlalchemy for ORM
- flask-migration : Alembic wrapper for db design changes from model definition
- flask config for app factory design
- flask blueprints for modules
- flask email and jinja templates
- flask testing
- flask-jwt / flask-login
- marshmallow for serialization of JSON

## Installation

Make sure you have these installed

```sh
apt install python3-venv
```

Create the virtual environment

```sh
python3 -m venv <venv-directory>
```

Install pip3 virtual environment

```sh
pip install virtualenv
```

## Working within virtual environment

Activate the virtual env

```sh
source venv/bin/activate
# returns:
# (venv) $
```

Installing packages ie. flask

```sh
pip install flask
```

Check dependencies

```sh
pip freeze
```

## Development server

To use the development server the environment variable FLASK_APP needs the path of the entry point

```sh
#!/bin/bash

export FLASK_APP=sersky.py
export FLASK_DEBUG=1
export FLASK_CONFIG=development
export SERVER_ADMIN=admin@email.com
```

Then you can run the development server

```sh
flask run
```

Can also be invoked within the application

```py
if __name__ = '__main__':
    < flask_instance >.run()
```

### Debug Mode

Set environment variable FLASK_DEBUG=1 and run

```sh
export FLASK_DEBUG=1
export FLASK_APP=sersky.py
flask run
```

## Database Operations

### Using Flask-Migrate

Initiate migrate:

```sh
flask db init
```

When changes are made to the models generate an automatic migration script.
**Review: the generated migration script for inaccuracies ie: (name changes resulting in deletions)**

```sh
flask db migrate
# add a comment
flask db migrate -m "changes made: ..."
```

Once you've reviewed and accepted the migration script, apply it to the database (for a first migration, equivalent to
db.create_all())
**note: the command will fail if the tables already exist and is the first time running the command. Another option
would be to run flask db stamp and mark the existing database as upgraded**:

```sh
flask db upgrade
flask db downgrade
```

## Using CLI commands

Create the database from models

```sh
flask db_create
```

Seed the database from json file

```sh
flask db_seed
```

Seed the database reference directory

```shell
flask db_reference_seed
```

Drop the database

```sh
flask db_drop
```
