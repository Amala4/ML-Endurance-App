from django.contrib import admin
from .models import (
    Support,
    Workout,
    WorkoutLog,
    WorkoutFuelLog,
    WorkoutCondition,
    FuelingIssue,
    FuelingPlan
)

admin.site.index_title = 'Site Administration'

# Workout admin set up
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'user', 'planned_date')
    list_display_links = ('name', 'sport', 'user')
    readonly_fields = ['date_added']
    search_fields = ('user__email',)
    list_filter = ('sport',)
admin.site.register(Workout, WorkoutAdmin)




# WorkoutLog admin set up
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('workout', 'duration', 'calories', 'date')
    list_display_links = ('workout', 'duration', 'calories', 'date')
    search_fields = ('workout__user__email', 'workout__name')
admin.site.register(WorkoutLog, WorkoutLogAdmin)




# WorkoutFuelLog admin set up
class WorkoutFuelLogAdmin(admin.ModelAdmin):
    list_display = ('workout_log', 'water', 'sodium', 'carbs', 'date_added')
    list_display_links = ('workout_log', 'water', 'sodium', 'carbs', 'date_added')
    readonly_fields = ('date_added',)
    search_fields = ('workout_log__workout__user__email', 'workout_log__workout__name')
admin.site.register(WorkoutFuelLog, WorkoutFuelLogAdmin)




# WorkoutCondition admin set up
class WorkoutConditionAdmin(admin.ModelAdmin):
    list_display = ('workout_log', 'weather_condition', 'isIndoors', 'date_added')
    list_display_links = ('workout_log', 'weather_condition', 'isIndoors', 'date_added')
    readonly_fields = ('date_added',)
    search_fields = ('workout_log__workout__user__email', 'workout_log__workout__name')
admin.site.register(WorkoutCondition, WorkoutConditionAdmin)




# FuelingIssues admin set up
class FuelingIssuesAdmin(admin.ModelAdmin):
    list_display = ('workout_log', 'bloating_gi', 'cramping', 'bonking', 'date_added')
    list_display_links = ('workout_log', 'bloating_gi', 'cramping', 'bonking', 'date_added')
    readonly_fields = ('date_added',)
    search_fields = ('workout_log__workout__user__email', 'workout_log__workout__name')
admin.site.register(FuelingIssue, FuelingIssuesAdmin)




# FuelingPlan admin set up
class FuelingPlanAdmin(admin.ModelAdmin):
    list_display = ('workout', 'water', 'sodium', 'carbs', 'date_added')
    list_display_links = ('workout', 'water', 'sodium', 'carbs', 'date_added')
    readonly_fields = ('date_added',)
    search_fields = ('workout__user__email', 'workout__name')
admin.site.register(FuelingPlan, FuelingPlanAdmin)




# Support admin set up
class SupportAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_sent')
    list_display_links = ('user', 'date_sent')
    readonly_fields = ['user', 'message', 'date_sent']
    search_fields = ('user__email', 'message')


    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
admin.site.register(Support, SupportAdmin)
