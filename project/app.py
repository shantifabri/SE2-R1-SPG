from project import create_app
from flask import render_template

app = create_app('flask.cfg')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host=('0.0.0.0'))

