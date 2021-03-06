from store_password_in_db.user import User


users = [
    User(1, 'Tom', 'abc123')
]
username_mapping = {user.username:user for user in users}
userid_mapping = {user.id:user for user in users}


def authenticate(username, password):
    user = User.get_user_by_name(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return User.get_user_by_id(user_id)