from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt #coz need create token
from src.config import Config
import uuid
import logging

from itsdangerous import URLSafeSerializer

passwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto",
)

ACCESS_TOKEN_EXPIRY = 3600 #1h in seconds

def generate_passwd_hash(password:str) -> str:
    password_hash = passwd_context.hash(password.encode('utf-8'))

    return str(password_hash)

def verify_password(password:str, hash:str) -> bool:
    return passwd_context.verify(str(password).encode('utf-8'),hash)


def create_access_token(user_data:dict, expiry:timedelta = None, refresh: bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(ACCESS_TOKEN_EXPIRY))

#now, need create unique UUID for each token
    payload['jti'] = str(uuid.uuid4()) #jti means jwt id

    payload['refresh'] = refresh

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET,
        algorithm = Config.JWT_ALGORITHM
    )

    return token

def decode_token(token:str) -> dict:
    try:
        token_data = jwt.decode(
            jwt = token,
            key = Config.JWT_SECRET,
            algorithms = [Config.JWT_ALGORITHM]
    )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None




def create_url_safe_token(data: dict): #take in data uw to send
    serializer = URLSafeSerializer(secret_key = Config.JWT_SECRET, salt = "email-configuration")
    
    token = serializer.dumps(data)
    
    return token


def decode_url_safe_token(token:str):
    serializer = URLSafeSerializer(secret_key = Config.JWT_SECRET, salt = "email-configuration")

    try:
        token_data = serializer.loads(token)
        
        return token_data
    
    except Exception as e:
        logging.error(str(e))
        
