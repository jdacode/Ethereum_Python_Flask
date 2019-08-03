from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from ether_ganache import Ganache

USER_LENGTH = 42
KEY_LENGTH = 64

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])  # Decorator
def get_node_ui():
    return send_from_directory('templates', 'index.html')

@app.route('/smartcontractsabi', methods=['GET'])  # Decorator
def smartcontractsabi():
    return send_from_directory('templates', 'smartcontracts_abi.html')

@app.route('/smartcontractsbytecode', methods=['GET'])  # Decorator
def smartcontractsbytecode():
    return send_from_directory('templates', 'smartcontracts_bytecode.html')

@app.route('/smartcontractsunderstanding', methods=['GET'])  # Decorator
def smartcontractsunderstanding():
    return send_from_directory('templates', 'smartcontracts_understanding.html')


@app.route('/ethereum_cryptocurrency', methods=['POST'])
def ethereum_cryptocurrency():
    values = request.get_json()
    recipient = values['recipient']
    sender = values['sender']
    key = values['key']
    amount = values['amount']
    if not values or recipient == "" or amount == "" or sender == "" or key == "":
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    if len(recipient) != USER_LENGTH:
        response = {
            'message': 'ID should be ' + str(USER_LENGTH) + ' digits long!!!'
        }
        return jsonify(response), 400
    if len(sender) != USER_LENGTH:
        response = {
            'message': 'ID should be ' + str(USER_LENGTH) + ' digits long!!!'
        }
        return jsonify(response), 400
    if len(key) != KEY_LENGTH:
        response = {
            'message': 'ID should be ' + str(KEY_LENGTH) + ' digits long!!!'
        }
        return jsonify(response), 400
    if str(amount).isdigit() is False:
        response = {
            'message': 'Amount must be only numbers!!!'
        }
        return jsonify(response), 400
    ganache.ganache_send_amount(sender, recipient, key, amount)
    conn, blocks = ganache.is_connected()
    response = {
        'message': "SENDER= " + sender + " " + "RECIPIENT= " + recipient + " " + "KEY= " + key + " " + "AMOUNT= " + str(amount),
        'message2': "GANACHE ............. Connection= " + str(conn) + " ............. " + " Blocks= " + str(blocks)
    }
    return jsonify(response), 201


@app.route('/smartcontracts_abi_write', methods=['POST'])
def smartcontracts_abi_write():
    values = request.get_json()
    smartcontract_address = values['contract']
    data = values['data']
    if not values or smartcontract_address == "" or data == "":
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    if len(smartcontract_address) != USER_LENGTH:
        response = {
            'message': 'ID should be ' + str(USER_LENGTH) + ' digits long!!!'
        }
        return jsonify(response), 400
    ganache.smart_contract_abi_write(smartcontract_address, data)
    conn, blocks = ganache.is_connected()
    response = {
        'message': "smartcontract_address= " + smartcontract_address,
        'message2': "GANACHE ............. Connection= " + str(conn) + " ............. " + " Blocks= " + str(blocks)
    }
    return jsonify(response), 201


@app.route('/smartcontracts_abi_read', methods=['POST'])
def smartcontracts_abi_read():
    values = request.get_json()
    smartcontract_address = values['contract']
    if not values or smartcontract_address == "":
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    if len(smartcontract_address) != USER_LENGTH:
        response = {
            'message': 'ID should be ' + str(USER_LENGTH) + ' digits long!!!'
        }
        return jsonify(response), 400
    data_read = ganache.smart_contract_abi_read(smartcontract_address)
    conn, blocks = ganache.is_connected()
    response = {
        'message': "ETHEREUM Blockchain data= " + data_read,
        'message2': "GANACHE ............. Connection= " + str(conn) + " ............. " + " Blocks= " + str(blocks)
    }
    return jsonify(response), 201


@app.route('/smartcontracts_abi_read_all', methods=['POST'])
def smartcontracts_abi_read_all():
    values = request.get_json()
    smartcontract_address = values['contract']
    if not values or smartcontract_address == "":
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    if len(smartcontract_address) != USER_LENGTH:
        response = {
            'message': 'ID should be ' + str(USER_LENGTH) + ' digits long!!!'
        }
        return jsonify(response), 400
    data_read1 = ganache.smart_contract_abi_read_all(smartcontract_address)
    data_read = ''.join(data_read1)
    print(data_read)
    conn, blocks = ganache.is_connected()
    response = {
        'message': "ETHEREUM Blockchain data:............." + data_read,
        'message2': "GANACHE ............. Connection= " + str(conn) + " ............. " + " Blocks= " + str(blocks)
    }
    return jsonify(response), 201


@app.route('/smartcontracts_bytecode', methods=['POST'])
def smartcontracts_bytecode():
    values = request.get_json()
    smartcontract_bytecode = values['contract']
    if not values or smartcontract_bytecode == "":
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    data_read = ganache.smart_contract_bytecode(smartcontract_bytecode)
    conn, blocks = ganache.is_connected()
    response = {
        'message': "ETHEREUM Blockchain data= " + data_read,
        'message2': "GANACHE ............. Connection= " + str(conn) + " ............. " + " Blocks= " + str(blocks)
    }
    return jsonify(response), 201


#port = os.getenv('VCAP_APP_PORT', '8000')
if __name__ == '__main__':
    ganache = Ganache()
    app.run()
