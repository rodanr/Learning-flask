from flask import Flask, jsonify, request, render_template
# Creating object of Flask class
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
stores =[
    {
        'name':'My Wonderful Store',
        'items':[
            {
                'name':'My Item',
                'price': 9.99
            }
        ]
    }
]

# POST - used to receive data from user 
# GET - used to send data back only/send data back to user
# In browser POST will use to send us data and GET to recive data but we are server so It's opposite with us

@app.route('/')
def home():
    return render_template('index.html') #Checks inside the same directory's templates folder

# POST /store data: {name}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')# 'http://127.0.01:5000/store/some_name'
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    
    return jsonify({'message':'store not found'})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})

# POST /store/<string:name>/item {name:,price:}
@app.route('/store/<string:name>/items', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name':request_data['name'],
                'price':request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store not found'})


#GET /store/<string:name>/item
@app.route('/store/<string:name>/items')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message':'store not found'})

app.run(port=5000)
