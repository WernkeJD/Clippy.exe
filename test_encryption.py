from encryption import *


generate_keys()
ip = encrypt_ip("1.23.45")
decrypted = decrypt_ip(ip)
print(decrypted)
