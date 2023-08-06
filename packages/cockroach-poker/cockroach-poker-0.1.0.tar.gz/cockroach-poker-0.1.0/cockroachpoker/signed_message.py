from Crypto import Random
from Crypto.Hash import MD5

class BadSignatureError(Exception):
    pass

rng = Random.new().read

def sign(sender, key, msg):
    return {
            'from': sender,
            'message': msg,
            'signature': key.sign(MD5.new(msg.encode('utf-8')).digest(), rng)
        }

def verify(key, signed_msg):
    if not key.verify(
            MD5.new(signed_msg['message'].encode('utf-8')).digest(),
            signed_msg['signature']):
        raise(BadSignatureError())
