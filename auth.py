import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def create_token(id: int) -> str:
    return jwt.encode({"id": id}, SECRET_KEY, algorithm=ALGORITHM)

def get_id(token: str) -> int:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})["id"]

def verify_token(token: str) -> bool:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.InvalidTokenError: # Invalid signature, token is not valid
        return False
    finally: # Didn't hit exception, so token is valid
        return True
    