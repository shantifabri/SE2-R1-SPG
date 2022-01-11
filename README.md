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
## How to run the telegram bot?

If you want to chat with our SPGR1 bot, you need to click this link: https://t.me/SPGR1bot firstly. And writing /start at the dialog box. Now you can send message and receive notifications with this bot.

This bot provides two basic command. When you input /info, you can get your telegram user id. Give this user id to ShopEmployee and she/he will bind this id with your SPG account, so that you can receive messages from our bot; When you input /balance, you can get the current balance of your account.

In addition to this, you can receive notifications from this bot at following scenarios:

a. When your order is confirmed;

b. When your balance is topped-up;

c. When your balance is insufficient to complete orders;

d. When the available products is updated.

------

## User Credentials:
| Role             | Name                | Email                          |
| ---------------- | ------------------- | ------------------------------ |
| Client           | Miriam Bread        | miriambread@yopmail.com        |
| Client           | Giovanni Fettuccini | giovannifettuccini@yopmail.com |
| Shop Employee    | Mario White         | mariowhite@yopmail.com         |
| Farmer           | Calvin Ross         | calvinross@yopmail.com         |
| Farmer           | Mike Garcia         | mikegarcia@yopmail.com         |
| Warehouse Worker | Bob Martin          | bobmartin@yopmail.com          |
| Warehouse Worker | Mark Doe            | markdoe@yopmail.com            |

Password for everyone: helloworld

----------
** The layout of the project, inizialization and tests are greatly based on [this repository](https://gitlab.com/patkennedy79/flask_user_management_example) by Patrick Kennedy.

