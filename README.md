# SE2-R1-SPG

Second project for Software Enineering II at PoliTo, group R1

----------

## How to run with docker?

Firstly, you should clone our project locally, and then switch to the project directory, cd to project directory and execute the following command: `'docker build -t se2r1/spg:v1 .'`

Waiting for the process of pulling the images, after finished, use `'docker images'`, you will find the image named se2r1/spg which you build before. Now execute `'docker run -p 41999:5000 se2r1/spg:v1'`in your bash to run, and then you can visit <http://127.0.0.1:41999/> to explore our project.

----------
## How to run locally?

You can run this project in a virtual env with the following commands:

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Start the development server

```
$ python application.py
```

Browse to http://127.0.0.1:5000

----------

## How to run the tests?

Tu run the tests in any mode, you need to be in the '/project' directory (where the file app.py is located).

To simply run the tests, execute the command `python -m pytest`.

If you want to see more details about the tests, you can run them in verbose mode using the flag -v as `python -m pytest -v`.

If instead you want to see the coverage of the suit of tests, you should run `python -m pytest --cov-report term-missing --cov=project`.

----------

** The layout of the project, inizialization and tests are greatly based on [this repository](https://gitlab.com/patkennedy79/flask_user_management_example) by Patrick Kennedy.
