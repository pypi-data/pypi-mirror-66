
from django.contrib import admin

from feedback.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = [
        'subject', 'id', 'user', 'name', 'mobile', 'email', 'date_created'
    ]

    search_fields = ['name', 'subject', 'mobile', 'email', 'text']

    fieldsets = (
        (None, {
            'fields': (
                'user',
                ('subject', 'name', ),
                ('mobile', 'email', ),
                'text',
            )
        }),
    )
