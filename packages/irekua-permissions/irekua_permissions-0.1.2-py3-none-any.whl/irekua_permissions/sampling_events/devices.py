def list(user, sampling_event=None, collection=None, **kwargs):
    if sampling_event is None and collection is None:
        return False

    if collection is None:
        collection = sampling_event.collection

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


def create(user, sampling_event=None, collection=None, **kwargs):
    if sampling_event is None and collection is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if collection is None:
        collection = sampling_event.collection

    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('add_collection_sampling_event')


def view(user, sampling_event_device=None, **kwargs):
    if sampling_event_device is None:
        return False

    collection = sampling_event_device.sampling_event.collection
    if collection.is_open:
        return True

    if not user.is_authenticated:
        return False

    if sampling_event_device.created_by == user:
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
    return role.has_permission('view_collection_sampling_events')


def change(user, sampling_event_device=None, **kwargs):
    if sampling_event_device is None:
        return False

    if not user.is_authenticated:
        return False

    if sampling_event_device.created_by == user:
        return True

    if user.is_superuser:
        return True

    collection = sampling_event_device.sampling_event.collection
    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('change_collection_sampling_events')


def delete(user, sampling_event_device=None, **kwargs):
    if sampling_event_device is None:
        return False

    if not user.is_authenticated:
        return False

    if sampling_event_device.created_by == user:
        return True

    if user.is_superuser:
        return True

    collection = sampling_event_device.sampling_event.collection
    if collection.collection_type.is_admin(user):
        return True

    return collection.is_admin(user)
