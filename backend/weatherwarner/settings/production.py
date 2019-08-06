import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa: F403 F401

HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "weatherwarner")

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", "https://c7671affe1554bbea8f097222ad5fb9f@sentry.io/1521057"),
    environment=f"{HEROKU_APP_NAME}.herokuapp.com",
    integrations=[DjangoIntegration()],
)

# HTTPS settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 7884000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Other security features
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
