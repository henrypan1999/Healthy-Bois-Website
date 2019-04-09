from flask import flash as flask_flash


def flash(obj):
    """
    Wraps flask.flash() providing handlers for more input types.
    str: flask.flash(obj)
    dict: for key in obj: for err in obj[key]: flash(err)
    list: for item in obj: flash(item)
    """

    if isinstance(obj, str):
        flask_flash(obj)
    elif isinstance(obj, dict):
        for key in obj:
            for err in obj[key]:
                flask_flash(err)
    elif isinstance(obj, list):
        for item in obj:
            flask_flash(item)
    else:
        raise ValueError(obj)
