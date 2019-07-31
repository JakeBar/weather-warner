from django.contrib import admin

from .models import PostalCode, Recipient

admin.site.register(Recipient)
admin.site.register(PostalCode)
