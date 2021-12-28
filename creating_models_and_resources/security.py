from creating_models_and_resources.models.user import UserModel


def authenticate(username, password):
    user = UserModel.get_user_by_name(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.get_user_by_id(user_id)