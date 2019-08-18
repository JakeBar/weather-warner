from django.contrib import admin

from .models import MessageChunk, PostalCode, Recipient


@admin.register(Recipient)
class Recipient(admin.ModelAdmin):
    list_filter = ("verified", "subscribed")
    list_display = ("name", "verified", "subscribed")


admin.site.register(PostalCode)
admin.site.register(MessageChunk)
