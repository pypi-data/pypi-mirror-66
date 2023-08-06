from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

class BadSignatureError(Exception):
    pass


def sign(sender, key, msg):
    signer = pkcs1_15.new(key)
    return {
            'from': sender,
            'message': msg,
            'signature': b64encode(pkcs1_15.new(key).sign(
                SHA256.new(msg.encode('utf-8')))).decode('utf-8')
        }

def verify(key, signed_msg):
    try:
        pkcs1_15.new(key).verify(
                SHA256.new(signed_msg['message'].encode('utf-8')),
                b64decode(signed_msg['signature'].encode('utf-8')))
    except (ValueError, TypeError):
        raise(BadSignatureError())
