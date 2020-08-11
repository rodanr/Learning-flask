from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank!")#addign argument to only get price key and value


    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        # item = next(filter(lambda x: x['name'] == name, items), None)#next gives the first item in the filter list and we are returning None if filter list hasn't anything to give
        # return {'item': item}, 200 if item else 404
        item = Item.find_by_name(name)
        if item:
            return item
        return {"message":"Item not found"}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item':{'name':row[0],'price':row[1]}}
        return None


    def post(self ,name):
        # returning message if user wants to create an item with the name that already exists
        #self.find_by_name can be used instead of Item.find_by_name
        if Item.find_by_name(name):
            return {'message':'An item with  name {} already exists'.format(name)}, 400
        # reques_data = request.get_json() #name is passed through url or route so avoiding json other than price as follow below
        request_data =  Item.parser.parse_args()
        new_item = {
            "name":name,
            "price":request_data["price"]
        }
        try :
            Item.insert_item(new_item)
        except:
            return {"message":"An error occured while inserting the item."}, 500 #Internal Server Error
        return new_item, 201 # 201 is for created

    @classmethod
    def insert_item(cls, new_item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (new_item['name'],new_item['price']))
        connection.commit()
        connection.close()


    def delete(self, name):
        if Item.find_by_name(name) is None:
            return {"message":"Item doesn't exists"}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"message":"Item deleted successfully"}

    def put(self, name):
        # request_data = request.get_json() not using it we don't want to replace the name here but only price
        request_data = Item.parser.parse_args()# arguments in json other than price will get ignored
        new_item = {
        'name':name,
        'price': request_data['price']
                }
        item = Item.find_by_name(name)
        if item is None:
            try:
                Item.insert_item(new_item)
            except Exception as e:
                return {"message":"An error occured while inserting the item."} , 500 #Internal Server Error
        else:
            try:
                Item.update(new_item)
            except Exception as e:
                return {"message":"An error occured while updating the item."} , 500 #Internal Server Error
        return new_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'],item['name']))
        connection.commit()
        connection.close()


class Items(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name":row[0],"price":row[1]})
        connection.close()
        return {'items':items}
