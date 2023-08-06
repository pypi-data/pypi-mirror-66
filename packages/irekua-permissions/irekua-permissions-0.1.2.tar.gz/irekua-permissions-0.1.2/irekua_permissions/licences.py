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

    if user.is_special:
        return True

    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def view(user, licence=None, **kwargs):
    if licence is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_special:
        return True

    collection = licence.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def change(user, licence=None, **kwargs):
    if licence is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    collection = licence.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def delete(user, licence=None, **kwargs):
    if licence is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    collection = licence.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)
