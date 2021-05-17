# Installation

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
export FLASK_APP=__init__.py
```

Then you can run the development server

```sh
flask run
```

Can also be invoked within the application

```py
if __name__ = '__main__':
    <flask_instance>.run()
```

### Debug Mode

Set environment variable FLASK_DEBUG=1 and run

```sh
export FLASK_DEBUG=1
export FLASK_APP=__init__.py
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

Once you've reviewed and accepted the migration script, apply it to the database (for a first migration, equivalent to db.create_all())
**note: the command will fail if the tables already exist and is the first time running the command. Another option would be to run flask db stamp and mark the existing database as upgraded**:

```sh
flask db upgrade
flask db downgrade
```

