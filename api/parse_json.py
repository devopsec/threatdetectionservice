from flask import make_response
import json

def json_decode(data):
    try:
        return json.loads(data)
    except:
        raise ValueError('Malformed JSON')

def json_encode(data):
    try:
        return json.dumps(data)
    except:
        raise ValueError('Malformed JSON')
    
def json_decode2(data):
    try:
        return json.JSONDecoder.decode(data)
    except:
        raise ValueError('Malformed JSON')

def json_encode2(data):
    try:
        return json.JSONEncoder.encode(data)
    except:
        raise ValueError('Malformed JSON')

def custom_json_output(data, code, headers=None):
    dumped = json.dumps(data, cls=CustomEncoder)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
