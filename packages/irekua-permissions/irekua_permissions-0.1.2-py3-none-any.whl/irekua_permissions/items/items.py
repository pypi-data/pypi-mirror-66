def list(user, collection=None, sampling_event=None,
        sampling_event_device=None, **kwargs):
    if collection is None:
        if sampling_event is not None:
            collection = sampling_event.collection

        if sampling_event_device is not None:
            collection = sampling_event_device.sampling_event.collection

    if collection is None:
        return False

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


def create(user, collection=None, sampling_event=None,
        sampling_event_device=None, **kwargs):

    if collection is None:
        if sampling_event is not None:
            collection = sampling_event.collection

        if sampling_event_device is not None:
            collection = sampling_event_device.sampling_event.collection

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
    return role.has_permission('add_collection_item')


def view(user, item=None, **kwargs):
    if item is None:
        return False

    if item.licence.licence_type.can_view:
        return True

    collection = item.sampling_event_device.sampling_event.collection
    if collection.is_open:
        return True

    if not user.is_authenticated:
        return False

    if item.created_by == user:
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
    return role.has_permission('view_collection_items')


def change(user, item=None, **kwargs):
    if item is None:
        return False

    if not user.is_authenticated:
        return False

    if item.created_by == user:
        return True

    if user.is_superuser:
        return True

    collection = item.sampling_event_device.sampling_event.collection
    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('change_collection_items')


def delete(user, item=None, **kwargs):
    if item is None:
        return False

    if not user.is_authenticated:
        return False

    if item.created_by == user:
        return True

    if user.is_superuser:
        return True

    collection = item.sampling_event_device.sampling_event.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)


def download(user, item=None, **kwargs):
    if item is None:
        return False

    if item.licence.licence_type.can_download:
        return True

    if not user.is_authenticated:
        return False

    if item.created_by == user:
        return True

    if user.is_superuser:
        return True

    collection = item.sampling_event_device.sampling_event.collection
    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('download_collection_items')


def view_thumbnail(user, item=None, **kwargs):
    if item is None:
        return False

    if item.licence.licence_type.can_view:
        return True

    collection = item.sampling_event_device.sampling_event.collection
    if collection.is_open:
        return True

    if not user.is_authenticated:
        return False

    if item.created_by == user:
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
    return role.has_permission('view_collection_items')
