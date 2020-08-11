from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from user import UserRegister
from security import authenticate, identity
from item import Item, Items

app = Flask(__name__)
api = Api(app)
app.secret_key = 'rown'

jwt = JWT(app, authenticate, identity) #/auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

#The py file which we run using command 'python file_name' then that file is __main__
#So avoiding to execute app.run() if this app.py file is imported by other python file 
if __name__ == '__main__':
    app.run(port=5000, debug=True)
