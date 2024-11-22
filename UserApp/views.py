from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from dateutil.parser import parse

from .models import (
    UserProfile,
    GENDER_CHOICES
)


#Global Constants
CustomUser = get_user_model()
admin_email = settings.DEFAULT_FROM_EMAIL
current_site = settings.FULL_DOMAIN

# For debugging on server only
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)




def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index') 
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'registration/login.html')
    
    return render(request, 'registration/login.html')




def sign_up(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        terms = request.POST.get('terms')

        if not (email and password and terms):
            messages.error(request, 'Email and Password are required, You must agree to the terms and privacy policy.')
            return render(request, 'registration/signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'registration/signup.html')
        
        user = CustomUser.objects.create_user(username=email, email=email, password=password)
        user.save()

        if user.pk:
            user.profile.name = fullname
            user.profile.save()
        else:
            messages.error(request, "There was an error creating your account.")

        auth.login(request, user)
        return redirect('profile')

    return render(request, 'registration/signup.html')




@login_required
def profile(request):

    try:
        profile = request.user.profile
        user_weight = profile.weight
        if user_weight:
            if profile.metrics_unit:
                user_weight = f"{user_weight}kg"
            else:
                imperial_weight = round(user_weight * 2.20462, 1)
                user_weight = f"{imperial_weight} lb"
        else:
            user_weight = None
    except:
        profile = None
        user_weight = None

    context = {
        'profile': profile,
        'user_weight': user_weight,
    } 

    if request.method == "POST":
            
        profile_pic = request.FILES.get('profile_pic')
        name = request.POST.get('name')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        ftp = request.POST.get('ftp')
        weight = request.POST.get('weight')
        units = request.POST.get('units')
        notifications = request.POST.get('notifications')

        profile, created = UserProfile.objects.get_or_create(user=request.user)


        # Profile Pic
        if profile_pic:
            try:
                image = Image.open(profile_pic)
                image.verify()
            except (IOError, SyntaxError):
                messages.error(request, 'Please Upload a Valid Image')
                return render(request, 'profile.html', context)

            compressed_profile_pic = compress_image(profile_pic) 
            profile.profile_pic = compressed_profile_pic
            

        # Name 
        if name: 
            if len(name) > 255:
                messages.error(request, 'Name is too long')
                return render(request, 'profile.html', context)
            profile.name = name


        # Birth Date
        if birth_date:
            try:
                birth_date = parse(birth_date).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                messages.error(request, 'Invalid Date Format')
                return render(request, 'profile.html', context)
            profile.birth_date = birth_date


        # Gender
        if gender: 
            if not gender in dict(GENDER_CHOICES):
                messages.error(request, 'Invalid Gender Choice')
                return render(request, 'profile.html', context)
            profile.gender = gender


        # Ftp
        if ftp: 
            ftp = float(ftp)
            if not (0 <= ftp <= 1000):
                messages.error(request, 'FTP is Invalid')
                return render(request, 'profile.html', context)
            profile.ftp = ftp

        
        # Units
        metrics_unit = bool(units == 'true')
        profile.metrics_unit = metrics_unit

        # Weight
        if weight:
            weight = float(weight)
            if metrics_unit:
                if not (0 <= weight <= 250):
                    messages.error(request, 'Invalid Weight figure, max is 250kg')
                    return render(request, 'profile.html', context)
            else: 
                if not (0 <= weight <= 550):
                    messages.error(request, 'Invalid Weight figure, max is 550lb')
                    return render(request, 'profile.html', context)
                weight = weight/2.20462
            profile.weight = weight


        # Notifications
        profile.notifications_enabled = notifications is not None


        # Email 
        if email: 
            if len(email) > 255:
                messages.error(request, 'Email is too long')
                return render(request, 'profile.html', context)
            request.user.email = email
            request.user.save()


        # Save profile
        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'profile.html', context)



@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        # user.delete() 
        # auth.logout(request)  
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("user_login") 
    
    return redirect("profile")




def compress_image(original_image):
    im = Image.open(original_image)
    im = ImageOps.exif_transpose(im)
    if im.mode != 'RGB':
        im = im.convert('RGB')

    im_io = BytesIO()
    im.save(im_io, format='JPEG')
    im_size = im_io.tell()

    max_size_bytes = 5 * 1024 * 1024  # 5MB
    if im_size <= max_size_bytes:
        return original_image  

    # If image size is greater than 5MB, compress it
    quality = 98 
    while im_size > max_size_bytes and quality > 10:
        im_io.seek(0) 
        im.save(im_io, format='JPEG', quality=quality, optimize=True)
        im_size = im_io.tell()
        quality -= 5  

    im_io.seek(0)
    compressed_image = InMemoryUploadedFile(
        im_io, 
        field_name="profile_pic", 
        name=original_image.name, 
        content_type='image/jpeg',
        size=im_size, 
        charset=None
    )

    return compressed_image
