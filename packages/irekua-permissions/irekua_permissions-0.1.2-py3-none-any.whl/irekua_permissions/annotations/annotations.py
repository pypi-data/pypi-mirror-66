def view(user, annotation=None, **kwargs):
    if annotation is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_special:
        return True

    if annotations.created_by == user:
        return True

    collection = (
        annotation
        .item
        .sampling_event_device
        .sampling_event
        .collection)
    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('view_collection_annotations')


def create(user, item=None, **kwargs):
    if item is None:
        return False

    if item.licence.licence_type.can_annotate:
        return True

    if not user.is_authenticated:
        return False

    if user.is_superuser | user.is_curator | user.is_model:
        return True

    if item.created_by == user:
        return True

    collection = (
        item
        .sampling_event_device
        .sampling_event
        .collection)
    if collection.collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('add_collection_annotations')


def change(user, annotation=None, **kwargs):
    if annotation is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if item.created_by == user:
        return True

    if not collection.is_user(user):
        return False

    role = collection.get_user_role(user)
    return role.has_permission('change_collection_annotations')


def delete(user, annotation=None, **kwargs):
    if annotation is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return item.created_by == user
