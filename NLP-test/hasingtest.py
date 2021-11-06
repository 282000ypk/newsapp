import hashlib

str = "\'jkd\' - fhdkfgf".encode()
hash_obj = hashlib.md5(str)
print(hash_obj.hexdigest())

