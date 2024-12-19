# from fastapi import Form, HTTPException, status
# from utils import jwt_utils
# from schemas.user import UserSchema


# user1 = UserSchema(
#     email="user1@gmail.com", password=jwt_utils.hash_password("user1")
# )
# user2 = UserSchema(
#     email="user2@gmail.com", password=jwt_utils.hash_password("user2")
# )
# users_db = {user1.email: user1, user2.email: user2}


# def validate_auth_user(username: str = Form(), password: str = Form()):
#     unauthed_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#     )

#     if not (user := users_db.get(username + "@gmail.com")):
#         raise unauthed_exception

#     if not jwt_utils.validate_password(
#         password=password, hashed_password=user.password
#     ):
#         raise unauthed_exception

#     return user
