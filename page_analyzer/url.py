import validators


def validate(url):
    errors_list = []
    if not validators.url(url) or len(url) > 255:
        errors_list.append("Некорректный URL")
        if not url:
            errors_list.append("URL обязателен")
        return errors_list
