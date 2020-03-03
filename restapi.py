from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'Codemart',
        'items': [
            {
                'name': 'shoe',
                'price': '5,555',
                'brand': 'addidas'
            }
        ]
    }
]

#POST/store data
@app.route('/store', methods= ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET/store/<strings:name>
@app.route('/store/<string:name>', methods= ['GET'])
def get_store(name):
    #iterate over the store 
    for store in stores:
    #if the store name matches, return it
        if store['name'] == name:
            return jsonify(store)
    # if none matches, return error msg 
    return jsonify({"message": "store not found"})

#GET?store
@app.route('/store', methods= ['GET'])
def get_stores():
    return jsonify({ 'stores':stores})

#POST/store/<strings:name>/item{name:,price:,brand:}
@app.route('/store/<string:name>/item', methods= ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price'],
                'brand': request_data['brand']
            } 
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


#GET/store/<strings:name>/item{name:,price:,brand:}
@app.route('/store/<string:name>/item', methods= ['GET'])
def get_items_in_store(name):
    #iterate over the store
    for store in stores:
    #if the store name matches, return it
        if store['name'] == name:
            return jsonify({'items': store['items']})
    #if none matches, return erro msg
    return jsonify ({'message': 'store not found'})



app.run(debug=True)