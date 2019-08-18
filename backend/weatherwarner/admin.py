from django.contrib import admin

from .models import MessageChunk, PostalCode, Recipient

admin.site.register(Recipient)
admin.site.register(PostalCode)
admin.site.register(MessageChunk)
