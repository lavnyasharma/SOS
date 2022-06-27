import json
import base64
def encode_id(**kwargs):
    payload = {}
    for key, value in kwargs.items():
        payload[key] = value
    str_payload = json.dumps(payload).encode('ascii')
    encoded_payload = str(base64.b64encode(str_payload)).split("'")[1]
    return encoded_payload


def decode_id(id):
    decoded = base64.b64decode(id)
    payload = json.loads(decoded)
    return payload


