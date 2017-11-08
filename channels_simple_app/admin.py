"""Admin site customizations"""

# pylint: disable=C0111,E0602,F0401,R0904,E1002

from django.contrib import admin

from channels_simple_app.models import IntegerValue


@admin.register(IntegerValue)
class IntegerValueAdmin(admin.ModelAdmin):
    """Admin Setup for IntegerValue"""
    list_display = ['name', 'value']
