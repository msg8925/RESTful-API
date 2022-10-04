from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashes a string passed to the function
def hash(password: str):
    return pwd_context.hash(password)

# Verifies that a plain and hashed password match
def  verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)