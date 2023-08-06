def view(user, collection=None, **kwargs):
    if collection.is_open:
        return True

    if not user.is_authenticated:
        return False

    if user.is_special:
        return True

    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    return collection.is_user(user)


def create(user, collection_type=None, **kwargs):
    if not user.is_authenticated:
        return False

    return collection_type.is_admin(user)


def change(user, collection=None, **kwargs):
    if not user.is_authenticated:
        return False

    if user.is_superuser | user.is_curator:
        return True

    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def delete(user, collection=None, **kwargs):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return collection.collection_type.is_admin(user)


def add_admin(user, collection=None, **kwargs):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return collection.collection_type.is_admin(user)


def delete_admin(user, collection=None, **kwargs):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return collection.collection_type.is_admin(user)
