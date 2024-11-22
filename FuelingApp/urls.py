from . import views
from django.urls import path, include



urlpatterns = [

    path('', views.index, name='index'),
    path('fuel-planner/', views.fuel_planner, name='fuel_planner'),
    path('home/', views.landing_page, name='landing_page'),
    path('workout-log/', views.workout_log, name='workout_log'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('notifications/', views.notifications, name='notifications'),
    path('chart-url/', views.get_chart_data, name='chart_url'),

]
