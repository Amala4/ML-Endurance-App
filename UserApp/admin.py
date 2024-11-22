from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import AdminUserCreationForm, AdminUserChangeForm
from .models import (
    CustomUser,
    UserProfile,
)
admin.site.unregister(Group)


class ModelSortingAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering1 = {
            "Workout": 1,
            "FuelingPlan": 2,
            "WorkoutLog": 3,
            "WorkoutFuelLog": 4,
            "WorkoutCondition": 5,
            "FuelingIssue": 6,
            "Support": 7,
        }

        ordering2 = {
            "CustomUser": 1,
            "UserProfile": 2,
        }


        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])

        for app in app_list:
            if app['app_label'] == 'FuelingApp':
                app['models'].sort(key=lambda x: ordering1[x['object_name']])

            if app['app_label'] == 'UserApp':
                app['models'].sort(key=lambda x: ordering2[x['object_name']])

        return app_list
admin.site.__class__ = ModelSortingAdminSite




# User admin set up
class CustomUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = CustomUser
    list_display = ('email',)
    search_fields = ('email',)
    ordering = ('-date_joined',)
    list_filter = ()
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        (None, {"fields": ('email', 'password', 'is_active')}),
        (_("Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )

    def response_add(self, request, obj, post_url_continue=None):
        msg = "The User was added successfully. Go to 'Pofile' section on the left column, select the profile and add more details"
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)
admin.site.register(CustomUser, CustomUserAdmin)




# UserProfile admin set up
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender')
    list_display_links = ('user', 'name', 'gender')
    readonly_fields = ['user', 'date_added', 'last_updated']
    list_filter = ['gender']
    search_fields = ('user__email', 'name')


    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(UserProfile, UserProfileAdmin)
