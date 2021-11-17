from project import create_app

# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app('flask.cfg')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host=('0.0.0.0'))