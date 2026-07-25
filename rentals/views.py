from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Property, Inquiry, VisitorLog, LOCATION_CHOICES, PROPERTY_TYPE_CHOICES

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_visitor(request, property_obj=None):
    try:
        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')
        VisitorLog.objects.create(
            ip_address=ip,
            page_url=request.path,
            property=property_obj,
            user_agent=ua[:500]
        )
    except Exception:
        pass

def home_view(request):
    log_visitor(request)
    featured_properties = Property.objects.filter(is_featured=True)[:6]
    if not featured_properties.exists():
        featured_properties = Property.objects.all()[:6]

    locations = LOCATION_CHOICES
    property_types = PROPERTY_TYPE_CHOICES

    # Handle Hero Form Submissions (Register or Login or Quick Search)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'register':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, f"Welcome to Rentora, {user.username}! Your VIP membership is active.")
                return redirect('dashboard')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
                    
        elif action == 'login':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password. Please try again.")

        elif action == 'inquiry':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            guests = request.POST.get('guests', 2)
            
            Inquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                guests=guests,
                message=message,
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Thank you! Our concierge team will contact you within 2 hours with curated options.")
            return redirect('home')

    context = {
        'featured_properties': featured_properties,
        'locations': locations,
        'property_types': property_types,
        'total_properties': Property.objects.count(),
    }
    return render(request, 'rentals/index.html', context)

def dashboard_view(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please sign in to access your member dashboard.")
        return redirect('login')

    log_visitor(request)
    
    # Retrieve user's inquiries/bookings
    user_inquiries = Inquiry.objects.filter(
        Q(email__iexact=request.user.email) | Q(name__icontains=request.user.username)
    ).distinct()

    if not user_inquiries.exists():
        user_inquiries = Inquiry.objects.all()[:5]

    # Property Search & Filter
    properties = Property.objects.all()
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    property_type = request.GET.get('property_type', '')
    max_price = request.GET.get('max_price', '')
    guests = request.GET.get('guests', '')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_display_name__icontains=query)
        )

    if location:
        properties = properties.filter(location=location)

    if property_type:
        properties = properties.filter(property_type=property_type)

    if max_price and max_price.isdigit():
        properties = properties.filter(price_per_night__lte=int(max_price))

    if guests and guests.isdigit():
        properties = properties.filter(max_guests__gte=int(guests))

    # Featured Properties (Compact Display)
    featured_properties = properties.filter(is_featured=True)[:4]
    if not featured_properties.exists():
        featured_properties = properties[:4]

    context = {
        'user_inquiries': user_inquiries,
        'featured_properties': featured_properties,
        'properties': properties,
        'locations': LOCATION_CHOICES,
        'property_types': PROPERTY_TYPE_CHOICES,
        'selected_location': location,
        'selected_type': property_type,
        'query': query,
        'max_price': max_price,
        'guests': guests,
    }
    return render(request, 'rentals/dashboard.html', context)

def properties_view(request):
    log_visitor(request)
    properties = Property.objects.all()

    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    property_type = request.GET.get('property_type', '')
    max_price = request.GET.get('max_price', '')
    guests = request.GET.get('guests', '')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_display_name__icontains=query)
        )

    if location:
        properties = properties.filter(location=location)

    if property_type:
        properties = properties.filter(property_type=property_type)

    if max_price and max_price.isdigit():
        properties = properties.filter(price_per_night__lte=int(max_price))

    if guests and guests.isdigit():
        properties = properties.filter(max_guests__gte=int(guests))

    context = {
        'properties': properties,
        'locations': LOCATION_CHOICES,
        'property_types': PROPERTY_TYPE_CHOICES,
        'selected_location': location,
        'selected_type': property_type,
        'query': query,
        'max_price': max_price,
        'guests': guests,
    }
    return render(request, 'rentals/properties.html', context)

def property_detail_view(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    log_visitor(request, property_obj=property_obj)
    similar_properties = Property.objects.filter(location=property_obj.location).exclude(id=property_obj.id)[:3]
    
    if not similar_properties.exists():
        similar_properties = Property.objects.exclude(id=property_obj.id)[:3]

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        check_in = request.POST.get('check_in') or None
        check_out = request.POST.get('check_out') or None
        guests = request.POST.get('guests', 2)
        message = request.POST.get('message', '')

        Inquiry.objects.create(
            property=property_obj,
            name=name,
            email=email,
            phone=phone,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            message=message,
            ip_address=get_client_ip(request)
        )
        messages.success(request, f"Your booking inquiry for '{property_obj.title}' has been submitted! Our concierge will get back to you shortly.")
        return redirect('property_detail', slug=property_obj.slug)

    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
    }
    return render(request, 'rentals/property_detail.html', context)

def register_view(request):
    log_visitor(request)
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Registration successful! Welcome to Rentora, {user.username}.")
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()

    return render(request, 'rentals/register.html', {'form': form})

def login_view(request):
    log_visitor(request)
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Logged in as {user.username}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'rentals/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
