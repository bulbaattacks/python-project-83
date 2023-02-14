import validators
from flask import flash, get_flashed_messages


def validate(url):
    if not validators.url(url) or len(url) > 255:
        flash("Некорректный URL", "danger")
        if not url:
            flash("URL обязателен", "danger")
        errors_list = get_flashed_messages(with_categories=True)
        return errors_list
