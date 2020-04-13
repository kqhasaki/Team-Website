from django.contrib import admin

from .models import Movie

from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Movie)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('name', 'directors', 'actors', 'mins', 'release_date')
