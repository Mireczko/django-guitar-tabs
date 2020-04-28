

def validate_tab_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.gp', '.gpx', '.gp5', '.gp4', '.gp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')