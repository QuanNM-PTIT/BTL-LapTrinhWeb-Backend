from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(request_pwd: str, user_pwd: str):
        return pwd_context.verify(request_pwd, user_pwd)
