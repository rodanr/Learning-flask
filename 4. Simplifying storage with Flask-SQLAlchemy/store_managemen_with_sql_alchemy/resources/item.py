from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank!")#addign argument to only get price key and value
    parser.add_argument('store_id',type=int,required=True,help="Every Item needs a store ID.")

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        # item = next(filter(lambda x: x['name'] == name, items), None)#next gives the first item in the filter list and we are returning None if filter list hasn't anything to give
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"Item not found"}



    def post(self ,name):
        # returning message if user wants to create an item with the name that already exists
        #self.find_by_name can be used instead of Item.find_by_name
        if ItemModel.find_by_name(name):
            return {'message':'An item with  name {} already exists'.format(name)}, 400
        # reques_data = request.get_json() #name is passed through url or route so avoiding json other than price as follow below
        request_data =  Item.parser.parse_args()
        new_item = ItemModel(name, request_data['price'], request_data['store_id'])#can be simplified to **reques_data
        try :
            new_item.save_to_db()
        except:
            return {"message":"An error occured while inserting the item."}, 500 #Internal Server Error
        return new_item.json(), 201 # 201 is for created



    def delete(self, name):
        item = ItemModel.find_by_name(name)#returns object
        if item:
            item.delete_from_db()
        return {"message":"Item deleted successfully"}

    def put(self, name):
        # request_data = request.get_json() not using it we don't want to replace the name here but only price
        request_data = Item.parser.parse_args()# arguments in json other than price will get ignored
        item = ItemModel.find_by_name(name)
        if item is None:
           item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']
        item.save_to_db()
        return item.json()


class Items(Resource):

    def get(self):

        return {'items':[item.json() for item in ItemModel.query.all()]}
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
