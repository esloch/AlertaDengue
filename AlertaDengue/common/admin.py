# Register your models here.
from django.contrib import admin
from .models import FederatedState


class FederatedStateAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'status']
    ordering = ['name']


admin.site.register(FederatedState, FederatedStateAdmin)
