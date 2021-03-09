from django.contrib import admin
from .models import Action

# Register your models here.

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """
        You just registered the Action model inte admin site.
        Run the localhost:8000/admin/actions/action/add/ in your browser
        for creating a new Action object
    """
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)