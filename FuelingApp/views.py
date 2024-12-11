from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db import transaction
import random
import json
from dateutil.parser import parse
from UserApp.models import UserProfile
from .models import (
    Support,
    Workout,
    WorkoutLog,
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
                return JsonResponse({'error': 'Invalid Sports Choice'}, status=200)


            # Planned Date
            if not planned_date_str:
                return JsonResponse({'error': 'Workout Planned date is required'}, status=200)
            try:
                planned_date = parse(planned_date_str).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid date format'}, status=200)


            # Duration
            try:
                duration = (duration_hours * 60) + duration_minutes
            except ValueError:
                return JsonResponse({'error': 'Invalid format for duration'}, status=200)


            # Training Stress
            if training_stress and (int(training_stress) > 10000):
                return JsonResponse({'error': 'Training stress score must be a number less than 10,000'}, status=200)

            training_stress = int(training_stress) if training_stress else None


            # Intensity Factor
            if intensity_factor and (float(intensity_factor) > 2):
                return JsonResponse({'error': 'Intensity Factor must be a number less than 2'}, status=200)
            intensity_factor = float(intensity_factor) if intensity_factor else None



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

            #Check if user prefers metric unit
            user_profile = UserProfile.objects.filter(user=request.user).first()
            prefers_metric = user_profile.metrics_unit

            if prefers_metric:
                water_unit = "ml"
                water_volume = fuel_plan["water"]
            else:
                water_unit = "oz"
                water_volume = round(fuel_plan["water"] / 29.5735, 2)

            fueling_requirements = {
                'carbohydrate': fuel_plan["carbs"],
                'water': water_volume,
                'water_unit': water_unit,
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
        if profile.metrics_unit:
            water_unit = "milliliters"
        else:
            water_unit = "ounces"
    except:
        profile = None
        water_unit = "milliliters"

    if request.method == "GET":
        context = {
            'latest_workout': latest_workout,
            'profile': profile,
            'water_unit': water_unit,
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


            with transaction.atomic():
                # Workout Date
                if not workout_date_str:
                    return JsonResponse({'error': 'Workout date is required'}, status=200)
                try:
                    workout_date = parse(workout_date_str).strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    return JsonResponse({'error': 'Invalid date format'}, status=200)


                # Duration
                try:
                    duration = (duration_hours * 60) + duration_minutes
                except ValueError:
                    return JsonResponse({'error': 'Invalid format for duration'}, status=200)


                # Training Stress
                if training_stress:
                    if  int(training_stress) > 10000:
                        return JsonResponse({'error': 'Training stress score must be a number less than 10,000'}, status=200)
                training_stress = int(training_stress) if training_stress else None


                # Calories
                if calories:
                    if float(calories) > 10000:
                        return JsonResponse({'error': 'Calories must be a number less than 10,000'}, status=200)
                calories = float(calories) if calories else None


                # Carbs Consumed
                carbs_consumed = float(carbs_consumed) if carbs_consumed else None

                # Water Consumed
                profile = request.user.profile
                if profile.metrics_unit:
                    water_consumed = float(water_consumed) if water_consumed else None
                else:
                    water_consumed = round(float(water_consumed) * 29.5735, 2) if water_consumed else None

                # Sodium Consumed
                if sodium_consumed:
                    if float(sodium_consumed) > 3000:
                        return JsonResponse({'error': 'Sodium consumed must be a number less than 3,000'}, status=200)
                sodium_consumed = float(sodium_consumed) if sodium_consumed else None


                # Weather Condition
                if not weather_condition in dict(WEATHER_CONDITION_CHOICES):
                    return JsonResponse({'error': 'Invalid weather condition'}, status=200)


                # Gastro Issue
                if not gastro_issue in dict(ISSUES_CHOICES):
                    return JsonResponse({'error': 'Invalid Gastro Issue Choice'}, status=200)


                # Muscle Cramp
                if not muscle_cramp in dict(ISSUES_CHOICES):
                    return JsonResponse({'error': 'Invalid Muscle Cramp Choice'}, status=200)


                # Gastro Issue
                if not bonking_issue in dict(ISSUES_CHOICES):
                    return JsonResponse({'error': 'Invalid Bonking Choice'}, status=200)


                # Save or update WorkoutLog
                workout_log, created = WorkoutLog.objects.update_or_create(
                    workout=latest_workout,
                    defaults={
                        'duration': duration,
                        'tss': training_stress,
                        'calories': calories,
                        'date': workout_date,
                    }
                )

                # Save or update WorkoutFuelLog
                WorkoutFuelLog.objects.update_or_create(
                    workout_log=workout_log,
                    defaults={
                        'water': water_consumed,
                        'sodium': sodium_consumed,
                        'carbs': carbs_consumed,
                    }
                )

                # Save or update WorkoutCondition
                WorkoutCondition.objects.update_or_create(
                    workout_log=workout_log,
                    defaults={
                        'weather_condition': weather_condition,
                        'isIndoors': indoor_workout,
                    }
                )

                # Save or update FuelingIssue
                FuelingIssue.objects.update_or_create(
                    workout_log=workout_log,
                    defaults={
                        'bloating_gi': gastro_issue,
                        'cramping': muscle_cramp,
                        'bonking': bonking_issue,
                    }
                )

                return JsonResponse({'success': 'Workout logged successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




@login_required
def check_workout_log(request):
    latest_workout = Workout.objects.filter(user=request.user).order_by('-date_added').first()
    existing_workout_log = WorkoutLog.objects.filter(workout=latest_workout).first()

    if existing_workout_log:
        return JsonResponse({'exists': True}, status=200)
    else:
        return JsonResponse({'exists': False}, status=200)




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
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'No profile found for this user'}, status=404)


    # Planned
    latest_workout = Workout.objects.filter(user=request.user).order_by('-date_added').first()
    if not latest_workout:
        return JsonResponse({'error': 'No workout found for this user'}, status=404)
    latest_workout_fuel_plan = get_object_or_404(FuelingPlan, workout=latest_workout)


    # Actual
    latest_workout_log = get_object_or_404(WorkoutLog, workout=latest_workout)
    latest_workout_fuel_log = get_object_or_404(WorkoutFuelLog, workout_log=latest_workout_log)

    if profile.metrics_unit:
        is_metric = True
        planned_water_consumption =latest_workout_fuel_plan.water
        actual_water_consumption =latest_workout_fuel_log.water
    else:
        is_metric = False
        planned_water_consumption = round(latest_workout_fuel_plan.water / 29.5735, 2)
        actual_water_consumption =round(latest_workout_fuel_log.water / 29.5735, 2)

    if latest_workout.sport in ['cycling', 'mountain_biking']:
        labels = ['TSS', 'Carbs', 'Water', 'Sodium']
        planned_data = [latest_workout.tss, latest_workout_fuel_plan.carbs, planned_water_consumption, latest_workout_fuel_plan.sodium]
        actual_data = [latest_workout_log.tss, latest_workout_fuel_log.carbs, actual_water_consumption, latest_workout_fuel_log.sodium]
    else:
        labels = ['Carbs', 'Water', 'Sodium']
        planned_data = [latest_workout_fuel_plan.carbs, planned_water_consumption, latest_workout_fuel_plan.sodium]
        actual_data = [latest_workout_fuel_log.carbs, actual_water_consumption, latest_workout_fuel_log.sodium]


    chart_data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Planned',
                'data': planned_data,
                'backgroundColor': '#2F388D',
                'barPercentage': 0.5,
                'categoryPercentage': 0.4,
                'borderRadius': 2,
            },
            {
                'label': 'Actual',
                'data': actual_data,
                'backgroundColor': '#7983D9',
                'barPercentage': 0.5,
                'categoryPercentage': 0.4,
                'borderRadius': 4,
            },
        ],
    }

    return JsonResponse({
        'success': 'Data Loaded successfully',
        'chart_data': chart_data,
        'is_metric': is_metric
    })




@login_required
def calculate_fuel_plan(workout):

    fueling_requirements = {
        'carbs': round(random.uniform(1, 30), 1),
        'water': round(random.uniform(1, 30), 1),
        'sodium': round(random.uniform(1, 30), 1),
    }

    return fueling_requirements
