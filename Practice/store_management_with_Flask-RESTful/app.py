from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'rodan'
items = []

jwt = JWT(app, authenticate, identity)

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', type = float, required = True, help = "This field cannot be empty")

	def get(self, name):
		item = next(filter(lambda x : x['name'] == name, items),None)
		if item :
			return item
		return {"message":"Item doesn't exist"}, 404

	def post(self, name):
		if next(filter(lambda x : x['name'] == name, items), None):
			return {"message":"Item with {} name, Already exists".format(name)}, 400
		parsed_data = Item.parser.parse_args()
		new_item = {
		"name":name,
		"price":parsed_data['price']
		}
		items.append(new_item)
		return new_item

	def put(self, name):
		parsed_data = Item.parser.parse_args()
		item = next(filter(lambda x : x['name'] == name, items), None)
		if item is not None:
			item.update(parsed_data)
			return item
		new_item = {
		"name":name,
		"price":parsed_data['price']
		}
		items.append(new_item)
		return new_item

	def delete(self, name):
		global items
		if next(filter(lambda x : x['name'] == name, items), None):
			items = list(filter(lambda x : x['name'] != name, items))
			return items
		else:
			return {"message":"Item with {} name doesn't exists".format(name)}, 404

class ItemList(Resource):
	@jwt_required()
	def get(self):
		return {"items":items}
		


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port = 5000, debug = True)
		
		