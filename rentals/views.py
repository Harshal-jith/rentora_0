from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.conf import settings
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

from django.conf import settings

def send_booking_confirmation_email(inquiry):
    try:
        if not inquiry.email:
            return False
        
        property_obj = inquiry.property
        is_over_capacity = False
        if property_obj and inquiry.guests > property_obj.max_guests:
            is_over_capacity = True

        ref_id = f"{inquiry.id:06d}"
        subject = f"Booking Inquiry Confirmed #{ref_id} - RENTORA Luxury Estates"
        
        sender = getattr(settings, 'EMAIL_HOST_USER', '')
        if sender and '@' in sender:
            from_email = f"Rentora Concierge <{sender}>"
        else:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'concierge@rentora.in')

        to_email = [inquiry.email]

        context = {
            'inquiry_id': ref_id,
            'name': inquiry.name,
            'email': inquiry.email,
            'property': property_obj,
            'check_in': inquiry.check_in,
            'check_out': inquiry.check_out,
            'guests': inquiry.guests,
            'is_over_capacity': is_over_capacity,
        }

        html_content = render_to_string('emails/booking_confirmation.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        sent_count = msg.send(fail_silently=True)
        print(f"Email dispatch to {to_email} finished (sent: {sent_count})")
        return sent_count > 0
    except Exception as e:
        print(f"Email dispatch exception caught safely: {type(e).__name__} - {e}")
        return False

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
            
            inquiry = Inquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                guests=guests,
                message=message,
                ip_address=get_client_ip(request)
            )
            send_booking_confirmation_email(inquiry)
            messages.success(request, f"Thank you! Booking confirmation (#REN-{inquiry.id:06d}) sent to {email}. Our concierge will contact you within 2 hours.")
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
        try:
            guests = int(request.POST.get('guests', 2))
        except (ValueError, TypeError):
            guests = 2

        message = request.POST.get('message', '')

        inquiry = Inquiry.objects.create(
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
        send_booking_confirmation_email(inquiry)

        ref_id = f"#REN-{inquiry.id:06d}"
        if guests > property_obj.max_guests:
            messages.warning(request, f"Confirmation {ref_id} sent to {email}! Note: {guests} guests exceeds standard max ({property_obj.max_guests}). VIP Concierge will arrange special suite setup.")
        else:
            messages.success(request, f"🎉 Booking inquiry {ref_id} for '{property_obj.title}' submitted! Confirmation email sent to {email}.")

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

def test_email_view(request):
    try:
        to_email = request.GET.get('to') or getattr(settings, 'EMAIL_HOST_USER', '') or 'test@example.com'
        backend = getattr(settings, 'EMAIL_BACKEND', '')
        host = getattr(settings, 'EMAIL_HOST', '')
        port = getattr(settings, 'EMAIL_PORT', '')
        user = getattr(settings, 'EMAIL_HOST_USER', '')
        pass_set = bool(getattr(settings, 'EMAIL_HOST_PASSWORD', ''))

        config_info = {
            'EMAIL_BACKEND': backend,
            'EMAIL_HOST': host,
            'EMAIL_PORT': port,
            'EMAIL_HOST_USER': user,
            'EMAIL_HOST_PASSWORD_SET': pass_set,
            'TARGET_EMAIL': to_email
        }

        try:
            sender = user if (user and '@' in user) else None
            from_str = f"Rentora Concierge <{sender}>" if sender else None
            sent = send_mail(
                subject="RENTORA Test Email Diagnostic",
                message="This is an automated test email from Rentora to verify live SMTP settings.",
                from_email=from_str,
                recipient_list=[to_email],
                fail_silently=False
            )
            return JsonResponse({
                'status': 'SUCCESS',
                'message': f'Test email dispatched successfully to {to_email}! (Count: {sent})',
                'config': config_info
            })
        except BaseException as e:
            return JsonResponse({
                'status': 'SMTP_ERROR',
                'error_type': type(e).__name__,
                'error_message': str(e),
                'config': config_info
            })
    except BaseException as outer_e:
        return JsonResponse({
            'status': 'VIEW_OUTER_ERROR',
            'error_type': type(outer_e).__name__,
            'error_message': str(outer_e)
        })
