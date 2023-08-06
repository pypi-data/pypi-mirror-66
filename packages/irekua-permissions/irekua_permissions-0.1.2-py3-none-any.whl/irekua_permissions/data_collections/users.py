def view(user, collection_user=None, **kwargs):
    if collection_user is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_special:
        return True

    collection = collection_user.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def create(user, collection=None, **kwargs):
    if collection is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def list(user, collection=None, **kwargs):
    if collection is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def change(user, collection_user=None, **kwargs):
    if collection_user is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    collection = collection_user.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def delete(user, collection_user=None, **kwargs):
    if collection_user is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    collection = collection_user.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)
