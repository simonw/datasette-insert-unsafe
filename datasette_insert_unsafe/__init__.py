from datasette import hookimpl


@hookimpl
def permission_allowed(action):
    if action == "insert:all":
        return True
