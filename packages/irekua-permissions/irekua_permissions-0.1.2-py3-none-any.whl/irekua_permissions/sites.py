def view(user, site=None, **kwargs):
    if site is None:
        return False

    if not user.is_authenticated:
        return False

    return site.created_by == user


def create(user, **kwargs):
    return user.is_authenticated


def change(user, site=None, **kwargs):
    if site is None:
        return False

    if not user.is_authenticated:
        return False

    return site.created_by == user


def delete(user, site=None, **kwargs):
    if site is None:
        return False

    if not user.is_authenticated:
        return False

    return site.created_by == user
