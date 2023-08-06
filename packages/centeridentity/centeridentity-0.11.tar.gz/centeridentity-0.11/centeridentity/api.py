import requests
import binascii
import base58
import base64
import os
import hashlib
import json
from coincurve.keys import PrivateKey, PublicKey
from coincurve import verify_signature
from eccsnacks.curve25519 import scalarmult_base
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2


class User:
    @classmethod
    def from_dict(cls, data):
        inst = cls()
        inst.public_key = data['public_key']
        inst.username = data['username']
        inst.username_signature = data['username_signature']
        return inst

    def generate_rid(self, username_signature):
        username_signatures = sorted(
            [
                str(self.username_signature),
                str(username_signature)
            ],
            key=str.lower
        )
        return hashlib.sha256((
            str(username_signatures[0]) + str(username_signatures[1])
        ).encode('utf-8')).digest().hex()

    @property
    def user_dict(self):
        return {
            'user_public_key': self.public_key_hex,
            'user_username_signature': self.username_signature,
            'user_username': self.username
        }

    @property
    def their_dict(self):
        return {
            'their_public_key': self.public_key_hex,
            'their_username_signature': self.username_signature,
            'their_username': self.username
        }

    @property
    def my_dict(self):
        return {
            'my_public_key': self.public_key_hex,
            'my_username_signature': self.username_signature,
            'my_username': self.username
        }

    @property
    def public_key_hex(self):
        if isinstance(self.public_key, PublicKey):
            return self.public_key.format().hex()
        else:
            return self.public_key


class Service(User):
    domain = 'http://0.0.0.0:8000'

    def __init__(self, wif, username):
        self.wif = wif
        self.key = PrivateKey.from_hex(binascii.hexlify(
            base58.b58decode(wif)
        )[2:-10].decode())
        self.public_key = self.key.public_key
        self.username = username
        self.username_signature = self.generate_service_username_signature()
        self.cipher_key = PBKDF2(hashlib.sha256(
            self.wif.encode('utf-8')
        ).hexdigest(), 'salt', 400).read(32)

    @classmethod
    def generate(cls, username):
        num = os.urandom(32).hex()
        wif = cls.to_wif(num)
        inst = cls(wif, username)
        inst.key = PrivateKey.from_hex(num)
        inst.public_key = inst.key.public_key
        inst.username = username
        inst.username_signature = base64.b64encode(
            inst.key.sign(inst.username.encode("utf-8"))
        ).decode("utf-8")
        return inst

    def generate_service_username_signature(self):
        signature = self.key.sign(self.username.encode('utf-8'))
        return base64.b64encode(signature).decode('utf-8')

    @classmethod
    def to_wif(cls, private_key: str):
        # to wif
        private_key_static = private_key
        extended_key = "80" + private_key_static + "01"
        first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
        second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
        final_key = extended_key + second_sha256[:8]
        return base58.b58encode(binascii.unhexlify(final_key)).decode('utf-8')

    def api_call(self, endpoint, data):
        api_token = requests.post(
            '{}{}'.format(self.domain, '/get-api-token'),
            json.dumps({
                'username_signature': self.username_signature
            }), headers={'content-type': 'application/json'}).json()
        if not api_token.get('api_uuid'):
            return {'status': 'error', 'message': 'api error'}
        request_signature = base64.b64encode(self.key.sign(hashlib.sha256(
            api_token['api_uuid'].encode()).hexdigest().encode())).decode("utf-8")
        return requests.post(
            '{}{}'.format(self.domain, endpoint),
            json.dumps(data),
            headers={
                'Authorization': 'basic {}'.format(
                    base64.b64encode(
                        '{}:{}'.format(
                            self.username_signature,
                            request_signature
                        ).encode()
                    ).decode("utf-8")
                ),
                'content-type': 'application/json'
            }
        ).json()

    @property
    def service_dict(self):
        return {
            'service_public_key': self.public_key.hex(),
            'service_username_signature': self.username_signature,
            'service_username': self.username
        }

    def encrypt_relationship(self, s):
        s = base64.b64encode(s.encode())
        from Crypto import Random
        BS = AES.block_size
        iv = Random.new().read(BS)
        s = s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
        cipher = AES.new(self.cipher_key, AES.MODE_CBC, iv)
        return (iv + cipher.encrypt(s)).hex()

    def decrypt_relationship(self, enc):
        enc = bytes.fromhex(enc)
        iv = enc[:16]
        cipher = AES.new(self.cipher_key, AES.MODE_CBC, iv)
        s = cipher.decrypt(enc[16:])
        return json.loads(base64.b64decode(s[0:-ord(s.decode('latin1')[-1])]))


class CenterIdentity:
    def __init__(self, wif, username='service'):
        self.service = Service(wif, username)

    @classmethod
    def generate(cls, username):
        service = Service.generate(username)
        return cls(
            service.wif,
            service.username
        )

    @classmethod
    def create_service(cls, username):
        return Service.generate(username)

    @classmethod
    def get_service(cls, username, wif):
        return Service(username, wif)

    @classmethod
    def from_dict(cls, data):
        return User.from_dict({
            'username': data['username'],
            'wif': data['wif']
        })

    @classmethod
    def user_from_dict(cls, data):
        return User.from_dict(data)

    def add_user(self, data):
        user = User.from_dict(data)
        a = os.urandom(32).decode('latin1')
        dh_public_key = scalarmult_base(a).encode('latin1').hex()
        dh_private_key = a.encode('latin1').hex()
        relationship = user.their_dict
        relationship.update(self.service.my_dict)
        relationship['dh_private_key'] = dh_private_key
        encrypted_relationship = self.service.encrypt_relationship(
            json.dumps(relationship)
        )
        extra_data = {
            'relationship': encrypted_relationship,
            'dh_public_key': dh_public_key
        }
        data.update(extra_data)
        return self.service.api_call(
            '/add-user',
            data
        )

    def get_user(self, data):
        rid = self.service.generate_rid(data['username_signature'])
        user_data = self.service.api_call(
            '/get-user',
            {
                'rid': rid
            }
        )
        user_data['relationship'] = self.service.decrypt_relationship(user_data['relationship'])
        return User.from_dict({
            'username': user_data['relationship']['their_username'],
            'public_key': user_data['relationship']['their_public_key'],
            'username_signature': user_data['relationship']['their_username_signature'],
        })

    def remove_user(self, data):
        data.update(self.to_dict)
        user_data = self.service.api_call(
            '/remove-user',
            data
        )
        return User.from_dict(user_data)

    @classmethod
    def authenticate(cls, session_id, post_data, hash_session_id=False):
        user = CenterIdentity.user_from_dict(post_data)
        if not isinstance(user, User):
            user = User.from_dict(user)
        if hash_session_id:
            session_id = hashlib.sha256(session_id.encode()).hexdigest()
        return verify_signature(
            base64.b64decode(post_data['session_id_signature']),
            session_id.encode(),
            bytes.fromhex(user.public_key)
        )
