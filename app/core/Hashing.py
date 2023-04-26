from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def password_hash(password:str):
    
    return pwd_context.hash(password)

#with this function we will verify if the password from the client it's equals to the one 
#related with the email to givin acces to the content related with the user registered in the 
#database
def verify_password(password:str,hashed_password):
    return pwd_context.verify(password,hashed_password)