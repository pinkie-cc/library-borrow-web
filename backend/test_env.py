from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["pbkdf2_sha256","bcrypt"], default="pbkdf2_sha256",pbkdf2_sha256__default_rounds=30000)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
print(hash_password("my password"))
