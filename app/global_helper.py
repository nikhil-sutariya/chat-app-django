from django.http import Http404
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def date_formatting(self):
    # sample date format - October 19, 2023
    if 'T' in self:
        return datetime.strptime(self.split('T')[0], '%Y-%m-%d').strftime('%B %e, %Y')

def get_or_raise(model, obj_id, error_message):
    if obj_id:
        try:
            return model.objects.get(id=obj_id)
        except:
            raise Http404(error_message)
    return model.objects.all()

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    key_pair = {
        "public_key": pem_public.decode('utf-8'),
        "private_key": pem_private.decode('utf-8')
    }
    return key_pair

def encrypt_message(message, public_key):
    # Encrypt the message using the public key
    print(public_key)
    if type(public_key) == str:
        public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            backend=default_backend()
        )

    cipher_text = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text

def decrypt_message(cipher_text, private_key):
    print(private_key)
    # Decrypt the message using the private key
    if type(private_key) == str:
        private_key = serialization.load_pem_private_key(
            private_key.encode('utf-8'),
            password=None,
            backend=default_backend()
        )

    plain_text = private_key.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode('utf-8')
    return plain_text
