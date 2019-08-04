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
