def list(user, **kwargs):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model


def view(user, model_version=None, **kwargs):
    if model_version is None:
        return True

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model


def create(user, **kwargs):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model


def delete(user, model_version=None, **kwargs):
    if model_version is None:
        return True

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model


def update(user, model_version=None, **kwargs):
    if model_version is None:
        return True

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.is_developer:
        return True

    return user.is_model
