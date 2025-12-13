from core.security import create_jwt_token, decode_jwt_token

data = {
    "name" : "jk",
    "age" : "23"
}


tok = create_jwt_token(data)
dat = decode_jwt_token(tok)

print(tok)
print(dat) 