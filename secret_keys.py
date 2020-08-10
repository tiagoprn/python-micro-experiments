import base64
import os

secret = base64.b64encode(os.urandom(60)).decode()
print(f'secret:\n{secret}')

