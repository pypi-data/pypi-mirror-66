def view(user, tool):
    return True


def create(user, tool):
    if user.is_superuser:
        return True

    return user.is_developer


def change(user, tool):
    if user.is_superuser:
        return True

    return user.is_developer


def delete(user, tool):
    if user.is_superuser:
        return True

    return user.is_developer
