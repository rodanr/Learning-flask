from flask import Flask
# Created an objct of flask using unique name
app = Flask(__name__)
# Created a route


@app.route('/')  # http://www.google.com/
# Created a simple home function
def home():
    return 'hello'


# Running the app
app.run(port=5000)
