import rsa
import os

def generate_keys():
    pub_key, priv_key = rsa.newkeys(512)
    with open("public.pem", "wb") as f:
        f.write(pub_key.save_pkcs1('PEM'))
    with open("private.pem", "wb") as f:
        f.write(priv_key.save_pkcs1('PEM'))

def load_public_key():
    with open("public.pem", "rb") as f:
        pub_key = rsa.PublicKey.load_pkcs1(f.read())
    return pub_key

def load_private_key_from_text(priv_key_text):
    return rsa.PrivateKey.load_pkcs1(priv_key_text.encode('utf-8'))

def encrypt_image(image_path):
    pub_key = load_public_key()
    encrypted_path = os.path.join("uploads", "encrypted_" + os.path.basename(image_path))

    with open(image_path, "rb") as f:
        data = f.read()

    encrypted_data = b""
    chunk_size = 53  # max chunk for 512-bit key with PKCS1
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        encrypted_data += rsa.encrypt(chunk, pub_key)

    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    return encrypted_path

def decrypt_image(encrypted_path, priv_key_text):
    priv_key = load_private_key_from_text(priv_key_text)
    decrypted_path = os.path.join("uploads", "decrypted_" + os.path.basename(encrypted_path))

    with open(encrypted_path, "rb") as f:
        data = f.read()

    decrypted_data = b""
    chunk_size = 64  # encrypted chunk size for 512-bit key
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        decrypted_data += rsa.decrypt(chunk, priv_key)

    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)

    return decrypted_path
