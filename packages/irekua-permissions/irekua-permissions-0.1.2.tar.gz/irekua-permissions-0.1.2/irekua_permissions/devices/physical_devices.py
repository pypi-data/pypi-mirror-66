def view(user, physical_device=None, **kwargs):
    if physical_device is None:
        return False

    if not user.is_authenticated:
        return False

    if user.is_special:
        return True

    return physical_device.created_by == user


def create(user, **kwargs):
    return user.is_authenticated


def change(user, physical_device=None, **kwargs):
    if physical_device is None:
        return False

    if not user.is_authenticated:
        return False

    return physical_device.created_by == user


def delete(user, physical_device=None, **kwargs):
    if physical_device is None:
        return False

    if not user.is_authenticated:
        return False

    return physical_device.created_by == user
