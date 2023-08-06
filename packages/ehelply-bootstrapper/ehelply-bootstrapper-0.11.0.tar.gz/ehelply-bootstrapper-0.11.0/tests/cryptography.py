from ehelply_bootstrapper.utils.cryptography import Encryption

encryption_cls: Encryption = Encryption([Encryption.generate_key()])

value = [{"day": "night"}]

enc: bytes = encryption_cls.encrypt(value)

print(enc)

print(encryption_cls.decrypt_list(enc))