LOCAL_APPS = (
    'core',
)

CONSTANCE_CONFIG = {
}

AUTH_USER_MODELS = [
    "core.User",
]

"""
    Set default auth user model from models list
    if AUTH_USER_MODELS is empty, set django user model by default
"""

AUTH_USER_MODEL = AUTH_USER_MODELS[0] if AUTH_USER_MODELS else 'auth.User'

LOGIN_REDIRECT_URL = 'ride-list'
LOGIN_URL = '/login/'


THUMBNAIL_PRESERVE_FORMAT = True

# Some autoslag handler that we need to create for make tests runnable


def auto_slag_handler():
    return 'auto_slug'

MOMMY_CUSTOM_FIELDS_GEN = {
    'django_extensions.db.fields.AutoSlugField': auto_slag_handler,
}
