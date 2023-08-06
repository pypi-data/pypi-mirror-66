def view(user, collection_device=None, **kwargs):
    if collection_device is None:
        return False

    collection = collection_device.collection
    if collection.is_open:
        return True

    if not user.is_authenticated:
        return False

    if collection_device.created_by == user:
        return True

    if user.is_special:
        return True

    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('view_collection_devices')


def create(user, collection=None, **kwargs):
    if collection is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    can = role.has_permission('add_collection_device')
    print('can', can)
    return can


def change(user, collection_device=None, **kwargs):
    if collection_device is None:
        return False

    if not user.is_authenticated:
        return False

    if collection_device.created_by == user:
        return True

    if user.is_superuser:
        return True

    collection = collection_device.collection
    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('change_collection_devices')


def delete(user, collection_device=None, **kwargs):
    if collection_device is None:
        return False

    if not user.is_authenticated:
        return False

    if collection_device.created_by == user:
        return True

    if user.is_superuser:
        return True

    collection = collection_device.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)
