from irekua_permissions.items import items


def list(user, **kwargs):
    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model


def view(user, model_prediction=None, **kwargs):
    if model_prediction is None:
        return True

    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    if user.is_model:
        return True

    item = model_prediction.item
    return items.view(user, item=item)


def create(user, **kwargs):
    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model


def delete(user, model_prediction=None, **kwargs):
    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model


def update(user, model_prediction=None, **kwargs):
    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model
