import validators


def validate(url):
    errors = []
    if not validators.url(url) or len(url) > 255:
        errors.append("Некорректный URL")
        if not url:
            errors.append("URL обязателен")
        return errors
