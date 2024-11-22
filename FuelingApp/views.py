from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from datetime import datetime
import random
import json
from dateutil.parser import parse
from .models import (
    Support,
    Workout,
    # CyclingWorkoutDetails,
    WorkoutLog,
    # CyclingWorkoutLog,
    WorkoutFuelLog,
    WorkoutCondition,
    FuelingIssue,
    FuelingPlan,
    WEATHER_CONDITION_CHOICES,
    ISSUES_CHOICES,
    SPORTS_CHOICES
)

sender_email = settings.DEFAULT_FROM_EMAIL
admin_email = settings.ADMIN_EMAIL


def landing_page(request):

    return render(request, 'landingPage.html')




@login_required
def index(request):
    try:
        profile = request.user.profile
    except:
        profile = None
    context = {
        'profile': profile,
    }

    return render(request, 'index.html', context)




@login_required
def fuel_planner(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            workout_name = data.get('workoutName')
            sport = data.get('sport')
            planned_date_str = data.get('plannedDate')
            duration_hours = int(data.get('duration_hours', 0) or 0)
            duration_minutes = int(data.get('duration_minutes', 0) or 0)
            training_stress = data.get('trainingStressScore')
            intensity_factor = data.get('intensityFactor')

            # Sports
            if sport and (not sport in dict(SPORTS_CHOICES)):
                return JsonResponse({'error': 'Invalid Sports Choice'}, status=400)


            # Planned Date
            if not planned_date_str:
                return JsonResponse({'error': 'Workout Planned date is required'}, status=400)
            try:
                planned_date = parse(planned_date_str).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid date format'}, status=400)


            # Duration
            try:
                duration = (duration_hours * 60) + duration_minutes
            except ValueError:
                return JsonResponse({'error': 'Invalid format for duration'}, status=400)
            

            # Training Stress
            if (not training_stress) or (int(training_stress) > 10000): 
                return JsonResponse({'error': 'Training stress score must be a number less than 10,000'}, status=400)
            training_stress = int(training_stress)


            # Intensity Factor
            if (not intensity_factor) or (float(intensity_factor) > 2): 
                return JsonResponse({'error': 'Intensity Factor must be a number less than 2'}, status=400)
            intensity_factor = float(intensity_factor)
        


            # Save workout data
            workout = Workout(
                name=workout_name,
                user=request.user,
                sport=sport,
                duration=duration,
                tss=training_stress,
                intensity_factor=intensity_factor,
                planned_date=planned_date,
            )

            # Get Fuel Plan
            fuel_plan = calculate_fuel_plan(workout)
            
            fueling_plan = FuelingPlan(
                workout=workout,
                water=fuel_plan["water"],
                sodium=fuel_plan["sodium"],
                carbs=fuel_plan["carbs"],
            )

            workout.save()
            fueling_plan.save()

            fueling_requirements = {
                'carbohydrate': fuel_plan["carbs"],
                'water': fuel_plan["water"],
                'sodium': fuel_plan["sodium"],
            }

            return JsonResponse({
                'success': 'Workout logged successfully',
                'fueling_requirements': fueling_requirements
            }, status=200)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    try:
        profile = request.user.profile
    except:
        profile = None    
    context = {
        'profile': profile,
    }

    return render(request, 'fuel_planner.html', context)




@login_required
def workout_log(request):
    latest_workout = Workout.objects.filter(user=request.user).order_by('-date_added').first()
    try:
        profile = request.user.profile
    except:
        profile = None   

    if request.method == "GET":
        context = {
            'latest_workout': latest_workout,
            'profile': profile,
        }
        return render(request, 'workout_log.html', context)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            # Workout Details
            workout_date_str = data.get('workout_date')
            duration_hours = int(data.get('duration_hours', 0) or 0)
            duration_minutes = int(data.get('duration_minutes', 0) or 0)
            training_stress = data.get('training_stress')
            calories = data.get('calories')

            # Fuel Log
            carbs_consumed = data.get('carbs_consumed')
            water_consumed = data.get('water_consumed')
            sodium_consumed = data.get('sodium_consumed')

            # Workout Condition
            weather_condition = data.get('weather')
            indoor_workout = str(data.get('indoor_workout')).lower() in ['true', '1', 'yes']

            # Workout Issues
            gastro_issue = int(data.get('gastro', 0) or 0)
            muscle_cramp = int(data.get('muscle', 0) or 0)
            bonking_issue = int(data.get('bonking', 0) or 0)



            # Workout Date
            if not workout_date_str:
                return JsonResponse({'error': 'Workout date is required'}, status=400)
            try:
                workout_date = parse(workout_date_str).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid date format'}, status=400)


            # Duration
            try:
                duration = (duration_hours * 60) + duration_minutes
            except ValueError:
                return JsonResponse({'error': 'Invalid format for duration'}, status=400)
            

            # Training Stress
            if training_stress:
                if  int(training_stress) > 10000: 
                    return JsonResponse({'error': 'Training stress score must be a number less than 10,000'}, status=400)
            training_stress = int(training_stress) if training_stress else None


            # Calories
            if calories:
                if float(calories) > 10000: 
                    return JsonResponse({'error': 'Calories must be a number less than 10,000'}, status=400)
            calories = float(calories) if calories else None

    
            # Carbs Consumed
            carbs_consumed = float(carbs_consumed) if carbs_consumed else None

            # Water Consumed
            water_consumed = float(water_consumed) if water_consumed else None 


            # Sodium Consumed
            if sodium_consumed:
                if float(sodium_consumed) > 3000: 
                    return JsonResponse({'error': 'Sodium consumed must be a number less than 3,000'}, status=400)
            sodium_consumed = float(sodium_consumed) if sodium_consumed else None


            # Weather Condition
            if not weather_condition in dict(WEATHER_CONDITION_CHOICES):
                return JsonResponse({'error': 'Invalid weather condition'}, status=400)


            # Gastro Issue
            if not gastro_issue in dict(ISSUES_CHOICES):
                return JsonResponse({'error': 'Invalid Gastro Issue Choice'}, status=400)


            # Muscle Cramp
            if not muscle_cramp in dict(ISSUES_CHOICES):
                return JsonResponse({'error': 'Invalid Muscle Cramp Choice'}, status=400)


            # Gastro Issue
            if not bonking_issue in dict(ISSUES_CHOICES):
                return JsonResponse({'error': 'Invalid Bonking Choice'}, status=400)


            

            # Save workout log data
            workout_log = WorkoutLog.objects.create(
                workout=latest_workout,
                duration=duration,
                tss=training_stress,
                calories=calories,
                date=workout_date,
            )

            # Save workout fuel log data
            WorkoutFuelLog.objects.create(
                workout_log=workout_log,
                water=water_consumed,
                sodium=sodium_consumed,
                carbs=carbs_consumed,
            )

            # Save workout conditions
            WorkoutCondition.objects.create(
                workout_log=workout_log,
                weather_condition=weather_condition,
                isIndoors=indoor_workout,
            )

            # Save workout fueling issues
            FuelingIssue.objects.create(
                workout_log=workout_log,
                bloating_gi=gastro_issue,
                cramping=muscle_cramp,
                bonking=bonking_issue,
            )

            return JsonResponse({'success': 'Workout logged successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




@login_required
def contact_us(request):
    if request.method == 'POST':
        message = request.POST.get('message')  
        attachment = request.FILES.get('attachment')

        if not message:
            messages.error(request, 'The message field cannot be empty.')
            return render(request, 'contact.html')

        if attachment:
            max_size = 50 * 1024 * 1024  
            if attachment.size > max_size:
                messages.error(request, 'The file size exceeds the 50MB limit.')
                return render(request, 'contact.html')

        Support.objects.create(
            user=request.user, 
            message=message,
            attachment=attachment,
        )

        send_mail(
            'New Support Message',
            f'You have a new support message from {request.user.email}: Login to your admin page to View message',
            sender_email,
            [admin_email], 
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully!')

    try:
        profile = request.user.profile
    except:
        profile = None   
    context = {
        'profile': profile,
    }
    return render(request, 'contact_us.html', context)




@login_required
def notifications(request):
    profile = request.user.profile
    context = {
        'profile': profile,
    }

    return render(request, 'notifications.html', context)



@login_required
def get_chart_data(request):
    latest_workout = Workout.objects.filter(user=request.user).order_by('-date_added').first()
    
    if not latest_workout:
        return JsonResponse({'error': 'No workout found for this user'}, status=404)

    latest_workout_fuel_plan = get_object_or_404(FuelingPlan, workout=latest_workout)
    latest_workout_log = get_object_or_404(WorkoutLog, workout=latest_workout)
    latest_workout_fuel_log = get_object_or_404(WorkoutFuelLog, workout_log=latest_workout_log)

    chart_data = {
        'labels': ['TSS', 'Carbs', 'Water', 'Sodium'],
        'datasets': [
            {
                'label': 'Planned',
                'data': [latest_workout.tss, latest_workout_fuel_plan.carbs, latest_workout_fuel_plan.water, latest_workout_fuel_plan.sodium],
                'backgroundColor': '#2F388D',
                'barPercentage': 0.5,
                'categoryPercentage': 0.4,
                'borderRadius': 2,
            },
            {
                'label': 'Actual',
                'data': [latest_workout_log.tss, latest_workout_fuel_log.carbs, latest_workout_fuel_log.water, latest_workout_fuel_log.sodium],
                'backgroundColor': '#7983D9',
                'barPercentage': 0.5,
                'categoryPercentage': 0.4,
                'borderRadius': 4,
            },
        ],
    }

    return JsonResponse({
        'success': 'Data Loaded successfully',
        'chart_data': chart_data
    })




@login_required
def calculate_fuel_plan(workout):

    fueling_requirements = {
        'carbs': round(random.uniform(1, 30), 1),
        'water': round(random.uniform(1, 30), 1),
        'sodium': round(random.uniform(1, 30), 1),
    }

    return fueling_requirements
