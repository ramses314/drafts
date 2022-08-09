from django.contrib import admin

# Register your models here.
from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'created')  #'target', ??????
    list_filter = ('created',)
    search_fields = ('verb', )
