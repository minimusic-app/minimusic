from pathlib import Path
from functools import wraps
try:
    from minimusic.config.userconfig import Config
    from minimusic.db.userdata import UserData
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from minimusic.config.userconfig import Config
    from minimusic.db.userdata import UserData

def admin_required():

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not "admin" in UserData.get_user_role["roles"]:
                return {"msg": "Only admins can do that!"}, 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper
