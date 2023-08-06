from .annotations import view as annotation_view

def view(user, vote):
    annotation = vote.annotation
    return annotation_view(user, annotation)


def create(user, annotation):
    if user.is_special:
        return True

    item = annotation.item
    licence = item.licence
    licence_type = licence.licence_type

    if not licence.is_active:
        return True

    if licence_type.can_vote_annotations:
        return True

    collection = item.collection
    collection_type = collection.collection_type

    if collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.has_user(user):
        return False

    return collection.has_permission(user, 'add_collection_annotation_vote')


def change(user, vote):
    pass
