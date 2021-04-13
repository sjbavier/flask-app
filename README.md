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