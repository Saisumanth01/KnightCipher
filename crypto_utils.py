from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

KEYS_DIR = "keys"

def generate_keys(name: str):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    os.makedirs(KEYS_DIR, exist_ok=True)

    private_key_path = os.path.join(KEYS_DIR, f"{name}_private.pem")
    public_key_path = os.path.join(KEYS_DIR, f"{name}_public.pem")

    with open(private_key_path, "wb") as priv_file:
        priv_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(public_key_path, "wb") as pub_file:
        pub_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print(f"Key pair '{os.path.basename(private_key_path)}' and '{os.path.basename(public_key_path)}' generated successfully in the '{KEYS_DIR}' directory.")

def rsa_encrypt(public_key_path: str, data: bytes) -> bytes:
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend()
        )

    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt(private_key_path: str, encrypted_data: bytes) -> bytes:
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

if __name__ == "__main__":
    try:
        key_name = input("Enter the name for the key pair: ").strip()
        if key_name:
            generate_keys(key_name)
        else:
            print("Key name cannot be empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
