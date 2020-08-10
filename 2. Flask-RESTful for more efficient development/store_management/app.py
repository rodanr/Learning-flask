from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'rown'

jwt = JWT(app, authenticate, identity) #/auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank!")#addign argument to only get price key and value


    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        item = next(filter(lambda x: x['name'] == name, items), None)#next gives the first item in the filter list and we are returning None if filter list hasn't anything to give
        return {'item': item}, 200 if item else 404
    
    def post(self ,name):
        # returning message if user wants to create an item with the name that already exists
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message':'An item with  name {} already exists'.format(name)}, 400
        
        # reques_data = request.get_json() #name is passed through url or route so avoiding json other than price as follow below
        request_data =  Item.parser.parse_args()
        new_item = {
            "name":name,
            "price":request_data["price"]
        }
        items.append(new_item)
        return new_item, 201 # 201 is for created

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':'Item deleted with name:{}'.format(name)}

    def put(self, name):
        # request_data = request.get_json() not using it we don't want to replace the name here but only price
        request_data = Item.parser.parse_args()# arguments in json other than price will get ignored
        item = next(filter(lambda x: x['name'] == name, items),None)
        if item is None:
            new_item = {
                'name':request_data['name'],
                'price': request_data['price']
            }
            items.append(new_item)
        else:
            item.update(request_data)
        return item

class Items(Resource):

    def get(self):
        return {'items':items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)