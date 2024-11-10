import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


##This section handles the creation and secure storage of the public and private keys

# Check if keys already exist to ensure that we only install them once
def generate_keys():

    # Check if key files already exist
    if os.path.exists("public_key.pem") and os.path.exists("private_key.pem") and os.path.getsize("public_key.pem") > 0 and os.path.getsize("private_key.pem") > 0:
        print("Keys already exist in the current directory. Not updating them.")
        
        # Read the existing public key
        with open("public_key.pem", "r") as f:
            public_pem = f.read()
        
        print("Here is your existing public key. Please share it with the person you would like to communicate with:")
        print(public_pem)

    else:
        # Generate a new RSA private key
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        # Serialize the private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Extract and serialize the public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        # Save the private key to a file
        with open("private_key.pem", "w") as f:
            f.write(private_pem)

        # Save the public key to a file
        with open("public_key.pem", "w") as f:
            f.write(public_pem)

        print("Keys have been generated and saved to 'public_key.pem' and 'private_key.pem'.")
        print("Here is your public key. Please share it with the person you would like to communicate with:")
        print(public_pem)


#used to encrypt messages with the users public key
def encrypt_ip(ip_address):

    with open("public_key.pem", "r") as f:
        public_pem = f.read()
        
    public_pem = public_pem.encode()

    public_key = serialization.load_pem_public_key(public_pem)

    encrypted_ip = public_key.encrypt(
        ip_address.encode(),
        padding.OAEP( 
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return encrypted_ip


#used to decrypt messages with the users private key
def decrypt_ip(encrypted_ip):
    with open("private_key.pem", "r") as f:
        private_pem = f.read()

    private_pem = private_pem.encode()

    private_key = serialization.load_pem_private_key(private_pem, password=None)

    decrypted_ip = private_key.decrypt(
        encrypted_ip,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return decrypted_ip.decode()