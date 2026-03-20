def prettify_label(value):
    if not value:
        return ""
    return value.replace("_", " ").strip().title()