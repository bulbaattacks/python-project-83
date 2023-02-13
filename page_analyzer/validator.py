import validators
from flask import flash, get_flashed_messages


def validation(data):
    if not validators.url(data) or len(data) > 255:
        flash("Некорректный URL", "danger")
        if not data:
            flash("URL обязателен", "danger")
        errors_list = get_flashed_messages(with_categories=True)
        return errors_list
