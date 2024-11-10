import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

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


# Encrypts the IP address using the user's public key
def encrypt_ip(ip_address, public_pem):

    # Remove any existing headers/footers and whitespace
    stripped_key = public_pem.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace(" ", "").replace("\n", "")
    
    # Insert newlines every 64 characters for PEM format
    formatted_key = "\n".join(stripped_key[i:i+64] for i in range(0, len(stripped_key), 64))
    
    # Add the BEGIN and END lines
    public_pem = f"-----BEGIN PUBLIC KEY-----\n{formatted_key}\n-----END PUBLIC KEY-----"

    # Convert the PEM key to bytes
    public_pem = public_pem.encode()

    # Load the public key
    public_key = serialization.load_pem_public_key(public_pem)

    # Encrypt the IP address
    encrypted_ip = public_key.encrypt(
        ip_address.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Encode the encrypted data in Base64
    encrypted_ip_base64 = base64.b64encode(encrypted_ip).decode('utf-8')

    return encrypted_ip_base64

# Decrypts the encrypted IP address using the user's private key
def decrypt_ip(encrypted_ip_base64):
    # Decode the Base64-encoded ciphertext
    encrypted_ip = base64.b64decode(encrypted_ip_base64)

    # Load the private key from the PEM file
    with open("private_key.pem", "r") as f:
        private_pem = f.read()

    private_pem = private_pem.encode()
    private_key = serialization.load_pem_private_key(private_pem, password=None)

    # Decrypt the IP address
    decrypted_ip = private_key.decrypt(
        encrypted_ip,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return decrypted_ip.decode('utf-8')