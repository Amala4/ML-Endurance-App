from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('non_binary', 'Non-Binary'),
    ('opt_out', 'Opt-Out')
]

ATHLETIC_HISTORY_CHOICES = [
    ('new', 'New (<6 months training)'),
    ('intermediate', 'Intermediate (6 months - 2 years training)'),
    ('advanced', 'Advanced (>2 years training)')
]



class CustomUser(AbstractUser):
    username = models.CharField(max_length=254, unique=True, blank=True,)
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    
    def save(self, *args, **kwargs):

        self.username = self.email
        is_new_user = not self.id
        super(CustomUser, self).save(*args, **kwargs)
        if is_new_user and not self.is_superuser:
            new_profile = UserProfile(user=self)
            new_profile.save() 


    def __str__(self):
        return self.email




class UserProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, verbose_name="User", primary_key=True, related_name='profile')
    name = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    ftp = models.FloatField("Functional Threshold Power(Ftp)", validators=[MinValueValidator(0), MaxValueValidator(1000)], null=True, blank=True)
    weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(250)], null=True, blank=True)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(150)], null=True, blank=True)
    gender = models.CharField(max_length=255,choices=GENDER_CHOICES, null=True, blank=True)
    sweat_rate = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(4)], help_text="Sweat rate in liters per hour", null=True, blank=True)
    sweat_composition = models.PositiveIntegerField(validators=[MaxValueValidator(3000)], help_text="Sweat composition in mg of sodium per liter.", null=True, blank=True)
    athletic_history = models.CharField(max_length=255,choices=ATHLETIC_HISTORY_CHOICES, help_text="Athletic experience level.", null=True, blank=True)
    notifications_enabled = models.BooleanField(default=True)
    metrics_unit = models.BooleanField("Metric Unit?", default=True, )
    birth_date = models.DateField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, )
    last_updated = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return f"Profile of {self.user.email}"
