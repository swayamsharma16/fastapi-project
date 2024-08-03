from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_text, hashed_pasword):
    return pwd_context.verify(plain_text, hashed_pasword)
