# Register your models here.
from django.contrib import admin
from common.models import FederatedState


class FederatedStateAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'status']
    ordering = ['name']


admin.site.register(FederatedState, FederatedStateAdmin)
