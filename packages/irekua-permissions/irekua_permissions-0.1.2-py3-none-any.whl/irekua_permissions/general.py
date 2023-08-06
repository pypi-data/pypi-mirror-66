def is_authenticated(user, **kwargs):
    return user.is_authenticated


def is_special(user, **kwargs):
    return user.is_special


def is_admin(user, **kwargs):
    return user.is_superuser


def is_model(user, **kwargs):
    return user.is_model


def is_developer(user, **kwargs):
    return user.is_developer


def is_curator(user, **kwargs):
    return user.is_curator


def owns_object(user, object=None, **kwargs):
    if object is None:
        return False

    return user == object.created_by


def is_collection_director(user, collection=None, **kwargs):
    if collection is None:
        return False

    return collection.collection_type.is_admin(user)


def is_collection_admin(user, collection=None, **kwargs):
    if collection is None:
        return False

    return collection.is_admin(user)


def is_collection_user(user, collection=None, **kwargs):
    if collection is None:
        return False

    return collection.is_user(user)
