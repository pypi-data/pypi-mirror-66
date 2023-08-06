from ehelply_bootstrapper.utils.cryptography import Encryption
from ehelply_bootstrapper.utils.secret import SecretManager

mykey: bytes = Encryption.generate_key()

encryption_cls: Encryption = Encryption([mykey])

value = [{"day": "night"}]

enc: bytes = encryption_cls.encrypt(value)

print(enc)

print(encryption_cls.decrypt_list(enc))

sm = SecretManager()
sm.add(mykey)
sm.add(mykey)
sm.add(mykey)
print(sm._secrets)
sm.remove(mykey)
print(sm._secrets)
