from passlib.context import CryptContext

print CryptContext([pbkdf2_sha512']).encrypt('123456')