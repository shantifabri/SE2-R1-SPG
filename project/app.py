from project import create_app
from flask import render_template

# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app('flask.cfg')

@app.route('/')
def index():
    return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True, port=5000, host=('0.0.0.0'))

if __name__ == '__main__':
    app.run(debug=True)