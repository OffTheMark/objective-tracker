from django.contrib import admin

from .models import Objective, TimeEntry


class TimeEntryInline(admin.StackedInline):
    model = TimeEntry
    extra = 0


class ObjectiveAdmin(admin.ModelAdmin):
    inlines = [TimeEntryInline]
    date_hierarchy = "date_created"
    list_display = ["name", "target", "date_created", "is_reached"]
    list_filter = ["date_created"]
    search_fields = ["name", "description"]


class TimeEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "date_created"
    list_display = ["explanation", "date_created"]
    list_filter = ["date_created"]
    search_fields = ["explanation"]


admin.site.register(Objective, ObjectiveAdmin)
admin.site.register(TimeEntry, TimeEntryAdmin)
