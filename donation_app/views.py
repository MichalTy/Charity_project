from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse

from .models import Donation, Institution, Category
from .forms import DonationForm


def LandingPage(request):
    """
    Renders the landing page with aggregated donation information and lists of organizations.
    """
    donation_count = Donation.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    supported_organizations_count = Donation.objects.values('institution').distinct().count()

    foundations = Institution.objects.filter(type=Institution.FOUNDATION).order_by('name')
    ngos = Institution.objects.filter(type=Institution.NGO).order_by('name')
    local_collections = Institution.objects.filter(type=Institution.COLLECTION_LOCAL).order_by('name')

    paginator_foundation = Paginator(foundations, 5)
    page_number_foundation = request.GET.get('page_foundation')
    foundations_paginated = paginator_foundation.get_page(page_number_foundation)

    paginator_ngo = Paginator(ngos, 5)
    page_number_ngo = request.GET.get('page_ngo')
    ngos_paginated = paginator_ngo.get_page(page_number_ngo)

    paginator_local_collection = Paginator(local_collections, 5)
    page_number_local_collection = request.GET.get('page_local_collection')
    local_collections_paginated = paginator_local_collection.get_page(page_number_local_collection)

    return render(request, 'index.html', {
        'donation_count': donation_count,
        'supported_organizations_count': supported_organizations_count,
        'foundations': foundations_paginated,
        'ngos': ngos_paginated,
        'local_collections': local_collections_paginated,
    })


def AddDonationView(request):
    """
    Renders the donation form and handles donation creation.
    """
    logged_user = request.user
    form = DonationForm()

    categories = Category.objects.all()
    institutions = Institution.objects.all()

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            categories = form.cleaned_data['categories']
            institution_id = form.cleaned_data['institution']
            institution = Institution.objects.get(pk=institution_id)
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            pick_up_date = form.cleaned_data['pick_up_date']
            pick_up_time = form.cleaned_data['pick_up_time']
            pick_up_comment = form.cleaned_data['pick_up_comment']
            user = logged_user if logged_user.is_authenticated else None

            donation = Donation.objects.create(
                quantity=quantity,
                institution=institution,
                address=address,
                phone_number=phone_number,
                city=city,
                zip_code=zip_code,
                pick_up_date=pick_up_date,
                pick_up_time=pick_up_time,
                pick_up_comment=pick_up_comment,
                user=user
            )

            donation.categories.set(categories)
            donation.save()

            return JsonResponse({'success': True, 'redirect_url': 'form_confirmation'})

        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'form.html', {
        'form': form, 'categories': categories, 'institutions': institutions
    })


def FormConfirmation(request):
    """
    Renders the confirmation page after a successful donation submission.
    """
    return render(request, 'form-confirmation.html')


def mark_donation_taken(request, donation_id):
    """
    Marks a donation as taken.
    """
    donation = get_object_or_404(Donation, pk=donation_id)
    donation.is_taken = True
    donation.save()
    return redirect('user_profile')


def DonationDetails(request, donation_id):
    """
    Renders the details page for a specific donation.
    """
    donation = get_object_or_404(Donation, pk=donation_id)
    return render(request, 'donation_details.html', {'donation': donation})


def Register(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            try:
                validate_password(password)
            except ValidationError as e:
                error_message = "Hasło nie spełnia wymagań: "
                for error in e:
                    error_message += error + " "
                return render(request, 'register.html', {'error_message': error_message,
                                                         'name': name, 'surname': surname, 'email': email})

            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.last_name = surname
            user.save()

            return redirect('login')
        else:
            return render(request, 'register.html', {'error_message': 'Hasła nie pasują do siebie.',
                                                     'name': name, 'surname': surname, 'email': email})

    return render(request, 'register.html')


def Login(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            return redirect('register')

    return render(request, 'login.html')


def Logout(request):
    """
    Handles user logout.
    """
    logout(request)
    return redirect('landing_page')


@login_required
def UserProfile(request):
    """
    Renders the user profile page.
    """
    user = request.user
    user_donations = Donation.objects.filter(user=user)

    return render(request, 'user_profile.html', {'user': user, 'user_donations': user_donations})


@login_required
def EditProfile(request):
    """
    Renders the edit profile page and handles profile updates.
    """
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')

        if not check_password(password, user.password):
            return render(request, 'edit_profile.html', {'error_message': 'Incorrect password'})

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('user_profile')

    return render(request, 'edit_profile.html', {'user': request.user})


@login_required
def ChangePassword(request):
    """
    Renders the change password page and handles password change.
    """
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if user.check_password(old_password) and new_password1 == new_password2:
            try:
                validate_password(new_password1, user=user)
            except ValidationError as e:
                return render(request, 'change_password.html', {'error_message': e})

            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('user_profile')
        else:
            pass

    return render(request, 'change_password.html')
