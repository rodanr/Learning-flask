from user import User
from werkzeug.security import safe_str_cmp
# users = [
#     {
#         'id':1,
#         'username':'rodan',
#         'password':'rodanrjn'
#     }
# ]
users = [
    User(1, 'rodan', 'rodanrjn')
]
# username_mapping = {
#     'rodan':{
#         'id':1,
#         'username':'rodan',
#         'password':'rodanrjn'
#     }
# }

#Set comprehension
username_mapping = {u.username: u for u in users}

# userid_mapping = {
#     1:{
#         'id':1,
#         'username':'rodan',
#         'password':'rodanrjn'
#     }
# }

userid_mapping = {u.id: u for u in users}
def authenticate(username, password):
    user = username_mapping.get(username, None)
    # if user is not None and user.password == password:
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

