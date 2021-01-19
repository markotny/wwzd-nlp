from flask import Flask
from flask import current_app, flash, jsonify, make_response, request
from enum import Enum
from random import randint
import recognition
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Party(Enum):
    KO = 1
    Konfederacja = 2
    Lewica = 3
    niez = 4
    PiS = 5
    PSLKukiz15 = 6

def make_my_response(obj):
    response = make_response(
        jsonify(
            obj
        ),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

def error_response():
    response = make_response(
        jsonify(
            {
                "messsage": "Something gone wrong",
                "severity": "A bit"
            }
        ),
        500
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/check_party_affiliation', methods=['POST', 'GET'])
def check_party_affiliation():
    json_obj = request.get_json(force=True)
    result = recognition.recognize(json_obj['query'].lower().split())
    obj = { 'response': result }
    return make_my_response(obj)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)