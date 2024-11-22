from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

WEATHER_CONDITION_CHOICES = [
    ('cold', 'Cold'),
    ('cool', 'Cool'),
    ('warm', 'Warm'),
    ('hot', 'Hot'),
    ('very_hot', 'Very Hot'),
]


ISSUES_CHOICES = [
    (0, 'None'),
    (5, 'Some'),
    (10, 'Severe'),
]

SPORTS_CHOICES = [
    ('cycling', 'Cycling'),
    ('mountain_biking', 'Mountain Biking'),
    ('running', 'Running'),
    ('xc_skiing', 'XC Skiing'),
]

class Workout(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='workout')
    sport = models.CharField(max_length=255, choices=SPORTS_CHOICES, null=True, blank=True)
    planned_date = models.DateField(null=True, blank=True)
    tss = models.PositiveIntegerField("Training Stress Score", validators=[MaxValueValidator(10000)], null=True, blank=True,)
    intensity_factor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(2)], null=True, blank=True)
    duration = models.PositiveIntegerField("Duration in Minutes", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        if self.name:
            return f"{self.name} workout"
        return self.user.email

    


class FuelingPlan(models.Model):
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE, related_name='fueling_plan')
    water = models.FloatField("Water (ml)", validators=[MinValueValidator(0),], null=True, blank=True,)
    sodium = models.FloatField("Sodium (mg)", validators=[MinValueValidator(0), MaxValueValidator(3000)], null=True, blank=True,)
    carbs = models.FloatField("Total Carbohydrates", validators=[MinValueValidator(0),], null=True, blank=True,)
    date_added = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name_plural = "Workout Fueling Plans"

    def __str__(self):
        if self.workout.name:
            return f"{self.workout.name} workout"
        return self.workout.user.email




# class CyclingWorkoutDetails(models.Model):
#     workout = models.OneToOneField(Workout, on_delete=models.CASCADE, related_name='workout_details')
#     intensity_factor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(2)], null=True, blank=True)
#     tss = models.PositiveIntegerField("Training Stress Score", validators=[MaxValueValidator(10000)], null=True, blank=True,)
#     date_added = models.DateTimeField(auto_now_add=True, )

#     def __str__(self):
#         if self.workout.name:
#             return self.workout.name
#         return self.workout.user.email



class WorkoutLog(models.Model):
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE, related_name='workout_log')
    duration = models.PositiveIntegerField("Duration in Minutes", null=True, blank=True)
    tss = models.PositiveIntegerField("Training Stress Score", validators=[MaxValueValidator(10000)], null=True, blank=True,)
    calories = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10000)], null=True, blank=True,)
    date = models.DateField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        if self.workout.name:
            return f"{self.workout.name} workout"
        return self.workout.user.email



# class CyclingWorkoutLog(models.Model):
#     workout_log = models.OneToOneField(WorkoutLog, on_delete=models.CASCADE, related_name='cycling_workout_log')
#     intensity_factor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(2)], null=True, blank=True)
#     tss = models.PositiveIntegerField("Training Stress Score", validators=[MaxValueValidator(10000)], null=True, blank=True,)
#     date_added = models.DateTimeField(auto_now_add=True, )

#     def __str__(self):
#         if self.workout_log.workout.name:
#             return self.workout_log.workout.name
#         return self.workout_log.workout.user.email



class WorkoutFuelLog(models.Model):
    workout_log = models.OneToOneField(WorkoutLog, on_delete=models.CASCADE, related_name='workout_fuel_log')
    water = models.FloatField("Water (ml)", validators=[MinValueValidator(0),], null=True, blank=True,)
    sodium = models.FloatField("Sodium (mg)", validators=[MinValueValidator(0), MaxValueValidator(3000)], null=True, blank=True,)
    carbs = models.FloatField("Total Carbohydrates", validators=[MinValueValidator(0),], null=True, blank=True,)
    date_added = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        if self.workout_log.workout.name:
            return f"{self.workout_log.workout.name} workout log"
        return self.workout_log.workout.user.email




class WorkoutCondition(models.Model):
    workout_log = models.OneToOneField(WorkoutLog, on_delete=models.CASCADE, related_name='workout_condition')
    weather_condition = models.CharField("Perceived Weather Condition", max_length=255, choices=WEATHER_CONDITION_CHOICES, null=True, blank=True)
    isIndoors = models.BooleanField("IsIndoors?", default=False)
    date_added = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name_plural = "Workout Condition Logs"

    def __str__(self):
        if self.workout_log.workout.name:
            return f"{self.workout_log.workout.name} workout log" 
        return self.workout_log.workout.user.email




class FuelingIssue(models.Model):
    workout_log = models.OneToOneField(WorkoutLog, on_delete=models.CASCADE, related_name='fueling_issues')
    bloating_gi = models.PositiveIntegerField("Bloating (GI)", validators=[MaxValueValidator(10)], choices=ISSUES_CHOICES, null=True, blank=True,)
    cramping = models.PositiveIntegerField("Cramping", validators=[MaxValueValidator(10)], choices=ISSUES_CHOICES, null=True, blank=True,)
    bonking = models.PositiveIntegerField("Bonking", validators=[MaxValueValidator(10)], choices=ISSUES_CHOICES, null=True, blank=True,)   
    date_added = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name_plural = "Fueling Issue Logs"

    def __str__(self):
        if self.workout_log.workout.name:
            return f"{self.workout_log.workout.name} workout log"
        return self.workout_log.workout.user.email




class Support(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='support_attachments/', blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name_plural = "Support Messages"

    def __str__(self):
        return self.user.email