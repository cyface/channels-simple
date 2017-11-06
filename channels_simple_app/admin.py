"""Admin site customizations for cardgame"""

# pylint: disable=C0111,E0602,F0401,R0904,E1002

from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """Admin Setup for Card"""
    date_hierarchy = 'date_created'
    list_display = ['name', 'type']

